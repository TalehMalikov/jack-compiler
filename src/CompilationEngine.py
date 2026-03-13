# CompilationEngine.py

from JackTokenizer import (
    JackTokenizer,
    TT_KEYWORD, TT_SYMBOL, TT_INT_CONST, TT_STRING_CONST, TT_IDENTIFIER,
)
from SymbolTable import SymbolTable
from VMWriter import VMWriter

OP_SET       = set('+-*/&|<>=')
UNARY_OP_SET = set('-~')
KEYWORD_CONSTS = {'true', 'false', 'null', 'this'}

OP_VM = {
    '+': 'add', '-': 'sub', '*': None,  # * and / use OS calls
    '/': None,  '&': 'and', '|': 'or',
    '<': 'lt',  '>': 'gt',  '=': 'eq',
}
UNARY_OP_VM = {'-': 'neg', '~': 'not'}


class CompilationEngine:

    def __init__(self, tokenizer):
        self._tok   = tokenizer
        self._sym   = SymbolTable()
        self._vm    = VMWriter()
        self._class_name   = ''
        self._label_count  = 0
        if self._tok.hasMoreTokens():
            self._tok.advance()

    def _newLabel(self):
        label = f'L{self._label_count}'
        self._label_count += 1
        return label

    def _eat(self, expected=None):
        """Consume current token (optionally assert its value) and advance."""
        val = self._tok.currentValue()
        if expected is not None and val != expected:
            raise SyntaxError(f'expected {expected!r}, got {val!r}')
        if self._tok.hasMoreTokens():
            self._tok.advance()
        return val

    def getOutput(self):
        return self._vm.getOutput()

    #  <<< class >>>>

    def compileClass(self):
        self._eat('class')
        self._class_name = self._eat()          # className
        self._eat('{')
        while self._tok.currentValue() in ('static', 'field'):
            self.compileClassVarDec()
        while self._tok.currentValue() in ('constructor', 'function', 'method'):
            self.compileSubroutine()
        self._eat('}')

    def compileClassVarDec(self):
        kind  = self._eat()                     # static | field
        type_ = self._eat()                     # type
        name  = self._eat()                     # varName
        self._sym.define(name, type_, kind)
        while self._tok.currentValue() == ',':
            self._eat(',')
            name = self._eat()
            self._sym.define(name, type_, kind)
        self._eat(';')

    #  <<< subroutine >>>>

    def compileSubroutine(self):
        self._sym.startSubroutine()
        kind = self._eat()                      # constructor | function | method
        ret_type = self._eat()                  # void | type
        name = self._eat()                      # subroutineName

        # methods receive 'this' as argument 0
        if kind == 'method':
            self._sym.define('this', self._class_name, 'arg')

        self._eat('(')
        self.compileParameterList()
        self._eat(')')
        self.compileSubroutineBody(name, kind)

    def compileParameterList(self):
        if self._tok.currentValue() != ')':
            type_ = self._eat()
            name  = self._eat()
            self._sym.define(name, type_, 'arg')
            while self._tok.currentValue() == ',':
                self._eat(',')
                type_ = self._eat()
                name  = self._eat()
                self._sym.define(name, type_, 'arg')

    def compileSubroutineBody(self, sub_name, kind):
        self._eat('{')
        while self._tok.currentValue() == 'var':
            self.compileVarDec()

        full_name = f'{self._class_name}.{sub_name}'
        n_locals  = self._sym.varCount('var')
        self._vm.writeFunction(full_name, n_locals)

        if kind == 'constructor':
            # allocate memory for the object
            n_fields = self._sym.varCount('field')
            self._vm.writePush('constant', n_fields)
            self._vm.writeCall('Memory.alloc', 1)
            self._vm.writePop('pointer', 0)         # anchor THIS

        elif kind == 'method':
            # set THIS to the object passed as argument 0
            self._vm.writePush('arg', 0)
            self._vm.writePop('pointer', 0)

        self.compileStatements()
        self._eat('}')

    def compileVarDec(self):
        self._eat('var')
        type_ = self._eat()
        name  = self._eat()
        self._sym.define(name, type_, 'var')
        while self._tok.currentValue() == ',':
            self._eat(',')
            name = self._eat()
            self._sym.define(name, type_, 'var')
        self._eat(';')

    # <<< statements >>>

    def compileStatements(self):
        while True:
            v = self._tok.currentValue()
            if   v == 'let':    self.compileLet()
            elif v == 'if':     self.compileIf()
            elif v == 'while':  self.compileWhile()
            elif v == 'do':     self.compileDo()
            elif v == 'return': self.compileReturn()
            else: break

    def compileLet(self):
        self._eat('let')
        var_name = self._eat()
        is_array = self._tok.currentValue() == '['

        if is_array:
            # push base address of array
            self._pushVar(var_name)
            self._eat('[')
            self.compileExpression()     # index
            self._eat(']')
            self._vm.writeArithmetic('add')   # base + index -> address on stack

        self._eat('=')
        self.compileExpression()         # RHS value now on stack
        self._eat(';')

        if is_array:
            self._vm.writePop('temp', 0)      # save value
            self._vm.writePop('pointer', 1)   # set THAT to address
            self._vm.writePush('temp', 0)     # restore value
            self._vm.writePop('that', 0)      # store
        else:
            self._popVar(var_name)

    def compileIf(self):
        label_else = self._newLabel()
        label_end  = self._newLabel()

        self._eat('if')
        self._eat('(')
        self.compileExpression()
        self._eat(')')
        self._vm.writeArithmetic('not')
        self._vm.writeIf(label_else)

        self._eat('{')
        self.compileStatements()
        self._eat('}')
        self._vm.writeGoto(label_end)

        self._vm.writeLabel(label_else)
        if self._tok.currentValue() == 'else':
            self._eat('else')
            self._eat('{')
            self.compileStatements()
            self._eat('}')
        self._vm.writeLabel(label_end)

    def compileWhile(self):
        label_start = self._newLabel()
        label_end   = self._newLabel()

        self._eat('while')
        self._vm.writeLabel(label_start)
        self._eat('(')
        self.compileExpression()
        self._eat(')')
        self._vm.writeArithmetic('not')
        self._vm.writeIf(label_end)

        self._eat('{')
        self.compileStatements()
        self._eat('}')
        self._vm.writeGoto(label_start)
        self._vm.writeLabel(label_end)

    def compileDo(self):
        self._eat('do')
        self._compileSubroutineCall()
        self._eat(';')
        self._vm.writePop('temp', 0)     # discard return value

    def compileReturn(self):
        self._eat('return')
        if self._tok.currentValue() != ';':
            self.compileExpression()
        else:
            self._vm.writePush('constant', 0)   # void return
        self._eat(';')
        self._vm.writeReturn()

    # <<< expressions >>>

    def compileExpression(self):
        self.compileTerm()
        while self._tok.currentValue() in OP_SET:
            op = self._eat()
            self.compileTerm()
            if op == '*':
                self._vm.writeCall('Math.multiply', 2)
            elif op == '/':
                self._vm.writeCall('Math.divide', 2)
            else:
                self._vm.writeArithmetic(OP_VM[op])

    def compileTerm(self):
        tt  = self._tok.tokenType()
        val = self._tok.currentValue()

        if tt == TT_INT_CONST:
            self._vm.writePush('constant', self._tok.intVal())
            self._eat()

        elif tt == TT_STRING_CONST:
            s = self._tok.stringVal()
            self._eat()
            self._vm.writePush('constant', len(s))
            self._vm.writeCall('String.new', 1)
            for ch in s:
                self._vm.writePush('constant', ord(ch))
                self._vm.writeCall('String.appendChar', 2)

        elif tt == TT_KEYWORD and val in KEYWORD_CONSTS:
            self._eat()
            if val == 'true':
                self._vm.writePush('constant', 0)
                self._vm.writeArithmetic('not')
            elif val in ('false', 'null'):
                self._vm.writePush('constant', 0)
            elif val == 'this':
                self._vm.writePush('pointer', 0)

        elif val == '(':
            self._eat('(')
            self.compileExpression()
            self._eat(')')

        elif val in UNARY_OP_SET:
            op = self._eat()
            self.compileTerm()
            self._vm.writeArithmetic(UNARY_OP_VM[op])

        elif tt == TT_IDENTIFIER:
            next_tok = self._tok.peek()
            if next_tok == '[':
                # array access
                self._pushVar(val)
                self._eat()          # varName
                self._eat('[')
                self.compileExpression()
                self._eat(']')
                self._vm.writeArithmetic('add')
                self._vm.writePop('pointer', 1)
                self._vm.writePush('that', 0)
            elif next_tok in ('(', '.'):
                self._compileSubroutineCall()
            else:
                self._pushVar(val)
                self._eat()

    def compileExpressionList(self):
        count = 0
        if self._tok.currentValue() != ')':
            self.compileExpression()
            count += 1
            while self._tok.currentValue() == ',':
                self._eat(',')
                self.compileExpression()
                count += 1
        return count

    #  <<< helpers >>> 

    def _compileSubroutineCall(self):
        name = self._eat()              # subroutineName | className | varName
        n_args = 0

        if self._tok.currentValue() == '.':
            self._eat('.')
            method_name = self._eat()
            kind = self._sym.kindOf(name)
            if kind is not None:
                # name is a variable -> instance method call
                self._pushVar(name)
                full_name = f'{self._sym.typeOf(name)}.{method_name}'
                n_args = 1              # 'this' is argument 0
            else:
                # name is a class -> static function / constructor call
                full_name = f'{name}.{method_name}'
        else:
            # unqualified call -> method on current object
            self._vm.writePush('pointer', 0)
            full_name = f'{self._class_name}.{name}'
            n_args = 1

        self._eat('(')
        n_args += self.compileExpressionList()
        self._eat(')')
        self._vm.writeCall(full_name, n_args)

    def _pushVar(self, name):
        kind  = self._sym.kindOf(name)
        index = self._sym.indexOf(name)
        self._vm.writePush(kind, index)

    def _popVar(self, name):
        kind  = self._sym.kindOf(name)
        index = self._sym.indexOf(name)
        self._vm.writePop(kind, index)