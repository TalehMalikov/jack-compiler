# VMWriter.py

SEGMENT_MAP = {
    'static'  : 'static',
    'field'   : 'this',
    'arg'     : 'argument',
    'var'     : 'local',
    'constant': 'constant',
    'this'    : 'this',
    'that'    : 'that',
    'pointer' : 'pointer',
    'temp'    : 'temp',
}


class VMWriter:

    def __init__(self):
        self._lines = []

    def writePush(self, segment, index):
        self._lines.append(f'push {SEGMENT_MAP[segment]} {index}')

    def writePop(self, segment, index):
        self._lines.append(f'pop {SEGMENT_MAP[segment]} {index}')

    def writeArithmetic(self, command):
        # command is one of: add sub neg eq gt lt and or not
        self._lines.append(command)

    def writeLabel(self, label):
        self._lines.append(f'label {label}')

    def writeGoto(self, label):
        self._lines.append(f'goto {label}')

    def writeIf(self, label):
        self._lines.append(f'if-goto {label}')

    def writeCall(self, name, nArgs):
        self._lines.append(f'call {name} {nArgs}')

    def writeFunction(self, name, nLocals):
        self._lines.append(f'function {name} {nLocals}')

    def writeReturn(self):
        self._lines.append('return')

    def getOutput(self):
        return '\n'.join(self._lines)