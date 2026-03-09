from JackTokenizer import (
    JackTokenizer,
    TT_KEYWORD, TT_SYMBOL, TT_INT_CONST, TT_STRING_CONST, TT_IDENTIFIER,
    _escape_xml,
)

OP_SET         = set('+-*/&|<>=')
UNARY_OP_SET   = set('-~')
KEYWORD_CONSTS = {'true', 'false', 'null', 'this'}


class CompilationEngine:

    def __init__(self, tokenizer):
        self._tok = tokenizer
        self._out = []
        self._indent = 0
        if self._tok.hasMoreTokens():
            self._tok.advance()

    # write opening tag and increase indent
    def _open(self, tag):
        self._out.append('  ' * self._indent + '<' + tag + '>')
        self._indent += 1

    # decrease indent and write closing tag
    def _close(self, tag):
        self._indent -= 1
        self._out.append('  ' * self._indent + '</' + tag + '>')

    # write current token as XML leaf and advance
    def writeToken(self):
        tt  = self._tok.tokenType()
        val = self._tok.currentValue()

        if tt == TT_STRING_CONST:
            val = _escape_xml(self._tok.stringVal())
        elif tt == TT_SYMBOL:
            val = _escape_xml(val)
        elif tt == TT_INT_CONST:
            val = str(self._tok.intVal())

        self._out.append('  ' * self._indent + '<' + tt + '> ' + val + ' </' + tt + '>')
        if self._tok.hasMoreTokens():
            self._tok.advance()

    def getXML(self):
        return '\n'.join(self._out)

    # <<< class >>>

    def compileClass(self):
        self._open('class')
        self.writeToken()   # class
        self.writeToken()   # className
        self.writeToken()   # {
        while self._tok.currentValue() in ('static', 'field'):
            self.compileClassVarDec()
        while self._tok.currentValue() in ('constructor', 'function', 'method'):
            self.compileSubroutine()
        self.writeToken()   # }
        self._close('class')

    def compileClassVarDec(self):
        self._open('classVarDec')
        self.writeToken()   # static | field
        self.writeToken()   # type
        self.writeToken()   # varName
        while self._tok.currentValue() == ',':
            self.writeToken()   # ,
            self.writeToken()   # varName
        self.writeToken()   # ;
        self._close('classVarDec')

    # <<< subroutine >>>

    def compileSubroutine(self):
        self._open('subroutineDec')
        self.writeToken()   # constructor | function | method
        self.writeToken()   # void | type
        self.writeToken()   # subroutineName
        self.writeToken()   # (
        self.compileParameterList()
        self.writeToken()   # )
        self.compileSubroutineBody()
        self._close('subroutineDec')

    def compileParameterList(self):
        self._open('parameterList')
        if self._tok.currentValue() != ')':
            self.writeToken()   # type
            self.writeToken()   # varName
            while self._tok.currentValue() == ',':
                self.writeToken()   # ,
                self.writeToken()   # type
                self.writeToken()   # varName
        self._close('parameterList')

    def compileSubroutineBody(self):
        self._open('subroutineBody')
        self.writeToken()   # {
        while self._tok.currentValue() == 'var':
            self.compileVarDec()
        self.compileStatements()
        self.writeToken()   # }
        self._close('subroutineBody')

    def compileVarDec(self):
        self._open('varDec')
        self.writeToken()   # var
        self.writeToken()   # type
        self.writeToken()   # varName
        while self._tok.currentValue() == ',':
            self.writeToken()   # ,
            self.writeToken()   # varName
        self.writeToken()   # ;
        self._close('varDec')

    # <<< statements >>>

    def compileStatements(self):
        self._open('statements')
        while True:
            v = self._tok.currentValue()
            if v == 'let':
                self.compileLet()
            elif v == 'if':
                self.compileIf()
            elif v == 'while':
                self.compileWhile()
            elif v == 'do':
                self.compileDo()
            elif v == 'return':
                self.compileReturn()
            else:
                break
        self._close('statements')

    def compileLet(self):
        self._open('letStatement')
        self.writeToken()   # let
        self.writeToken()   # varName
        if self._tok.currentValue() == '[':
            self.writeToken()   # [
            self.compileExpression()
            self.writeToken()   # ]
        self.writeToken()   # =
        self.compileExpression()
        self.writeToken()   # ;
        self._close('letStatement')

    def compileIf(self):
        self._open('ifStatement')
        self.writeToken()   # if
        self.writeToken()   # (
        self.compileExpression()
        self.writeToken()   # )
        self.writeToken()   # {
        self.compileStatements()
        self.writeToken()   # }
        if self._tok.currentValue() == 'else':
            self.writeToken()   # else
            self.writeToken()   # {
            self.compileStatements()
            self.writeToken()   # }
        self._close('ifStatement')

    def compileWhile(self):
        self._open('whileStatement')
        self.writeToken()   # while
        self.writeToken()   # (
        self.compileExpression()
        self.writeToken()   # )
        self.writeToken()   # {
        self.compileStatements()
        self.writeToken()   # }
        self._close('whileStatement')

    def compileDo(self):
        self._open('doStatement')
        self.writeToken()   # do
        self.writeToken()   # subroutineName | className | varName
        if self._tok.currentValue() == '.':
            self.writeToken()   # .
            self.writeToken()   # subroutineName
        self.writeToken()   # (
        self.compileExpressionList()
        self.writeToken()   # )
        self.writeToken()   # ;
        self._close('doStatement')

    def compileReturn(self):
        self._open('returnStatement')
        self.writeToken()   # return
        if self._tok.currentValue() != ';':
            self.compileExpression()
        self.writeToken()   # ;
        self._close('returnStatement')

    # <<< expressions >>>

    def compileExpression(self):
        self._open('expression')
        self.compileTerm()
        while self._tok.currentValue() in OP_SET:
            self.writeToken()   # op
            self.compileTerm()
        self._close('expression')

    def compileTerm(self):
        self._open('term')
        tt  = self._tok.tokenType()
        val = self._tok.currentValue()

        if tt == TT_INT_CONST:
            self.writeToken()
        elif tt == TT_STRING_CONST:
            self.writeToken()
        elif tt == TT_KEYWORD and val in KEYWORD_CONSTS:
            self.writeToken()
        elif val == '(':
            self.writeToken()   # (
            self.compileExpression()
            self.writeToken()   # )
        elif val in UNARY_OP_SET:
            self.writeToken()   # unary op
            self.compileTerm()
        elif tt == TT_IDENTIFIER:
            next_tok = self._tok.peek()
            if next_tok == '[':
                self.writeToken()   # varName
                self.writeToken()   # [
                self.compileExpression()
                self.writeToken()   # ]
            elif next_tok in ('(', '.'):
                self.writeToken()   # subroutineName | className
                if self._tok.currentValue() == '.':
                    self.writeToken()   # .
                    self.writeToken()   # subroutineName
                self.writeToken()   # (
                self.compileExpressionList()
                self.writeToken()   # )
            else:
                self.writeToken()   # plain variable

        self._close('term')

    def compileExpressionList(self):
        self._open('expressionList')
        if self._tok.currentValue() != ')':
            self.compileExpression()
            while self._tok.currentValue() == ',':
                self.writeToken()   # ,
                self.compileExpression()
        self._close('expressionList')