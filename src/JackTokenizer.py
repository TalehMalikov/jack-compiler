import re

KEYWORDS = {
    'class', 'constructor', 'function', 'method', 'field', 'static',
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
    'this', 'let', 'do', 'if', 'else', 'while', 'return'
}

SYMBOLS = set('{}()[].,;+-*/&|<>=~')

# token type constants
TT_KEYWORD      = 'keyword'
TT_SYMBOL       = 'symbol'
TT_INT_CONST    = 'integerConstant'
TT_STRING_CONST = 'stringConstant'
TT_IDENTIFIER   = 'identifier'

# single regex that matches all token types and comments at once
_TOKEN_RE = re.compile(
    r'"[^"]*"'                      # string constant
    r'|//[^\n]*'                    # single-line comment (will be skipped)
    r'|/\*.*?\*/'                   # block comment (will be skipped)
    r'|[{}()\[\].,;+\-*/&|<>=~]'   # symbol
    r'|[0-9]+'                      # integer constant
    r'|[A-Za-z_]\w*'               # identifier or keyword
    , re.DOTALL
)


class JackTokenizer:

    def __init__(self, source):
        # collect all tokens, skip comments
        self._tokens = []
        for m in _TOKEN_RE.finditer(source):
            tok = m.group(0)
            if tok.startswith('//') or tok.startswith('/*'):
                continue
            self._tokens.append(tok)
        self._pos = -1
        self._current = ''  # dummy value
    def hasMoreTokens(self):
        return self._pos < len(self._tokens) - 1

    def advance(self):
        self._pos += 1
        self._current = self._tokens[self._pos]

    def peek(self):
        # look at next token without consuming it
        if self._pos < len(self._tokens) - 1:
            return self._tokens[self._pos + 1]
        return None

    def tokenType(self) -> str:
        tok = self._current
        if tok in KEYWORDS:
            return TT_KEYWORD
        if tok in SYMBOLS:
            return TT_SYMBOL
        if tok[0].isdigit():
            return TT_INT_CONST
        if tok.startswith('"'):
            return TT_STRING_CONST
        return TT_IDENTIFIER

    def keyword(self) -> str:
        return self._current

    def symbol(self) -> str:
        return self._current

    def identifier(self) -> str:
        return self._current

    def intVal(self) -> int:
        return int(self._current)

    def stringVal(self) -> str:
        # remove the surrounding quotes
        return self._current[1:-1]

    def currentValue(self):
        return self._current

    def currentXML(self):
        tt = self.tokenType()
        if tt == TT_KEYWORD:
            val = self.keyword()
        elif tt == TT_SYMBOL:
            val = _escape_xml(self.symbol())
        elif tt == TT_INT_CONST:
            val = str(self.intVal())
        elif tt == TT_STRING_CONST:
            val = _escape_xml(self.stringVal())
        else:
            val = _escape_xml(self.identifier())
        return '<' + tt + '> ' + val + ' </' + tt + '>'


def _escape_xml(s):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    return s


def tokenize_to_xml(source):
    tok = JackTokenizer(source)
    lines = ['<tokens>']
    while tok.hasMoreTokens():
        tok.advance()
        lines.append(tok.currentXML())
    lines.append('</tokens>')
    return '\n'.join(lines)