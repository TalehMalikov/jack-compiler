# SymbolTable.py

CLASS_SCOPE = {'static', 'field'}
SUBROUTINE_SCOPE = {'arg', 'var'}


class SymbolTable:

    def __init__(self):
        self._class_table = {}       # name -> (type, kind, index)
        self._subroutine_table = {}
        self._counts = {'static': 0, 'field': 0, 'arg': 0, 'var': 0}

    def startSubroutine(self):
        """Reset subroutine-level scope. Call at the start of each subroutine."""
        self._subroutine_table = {}
        self._counts['arg'] = 0
        self._counts['var'] = 0

    def define(self, name, type_, kind):
        """Register a new variable. kind is 'static','field','arg', or 'var'."""
        index = self._counts[kind]
        self._counts[kind] += 1
        if kind in CLASS_SCOPE:
            self._class_table[name] = (type_, kind, index)
        else:
            self._subroutine_table[name] = (type_, kind, index)

    def varCount(self, kind):
        """Number of variables defined for the given kind."""
        return self._counts[kind]

    def _lookup(self, name):
        if name in self._subroutine_table:
            return self._subroutine_table[name]
        if name in self._class_table:
            return self._class_table[name]
        return None

    def typeOf(self, name):
        entry = self._lookup(name)
        return entry[0] if entry else None

    def kindOf(self, name):
        entry = self._lookup(name)
        return entry[1] if entry else None  # None = class/subroutine name, not a variable

    def indexOf(self, name):
        entry = self._lookup(name)
        return entry[2] if entry else None