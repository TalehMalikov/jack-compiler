# JackCompiler.py

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def compile_file(jack_path):
    source = jack_path.read_text(encoding='utf-8')
    tokenizer = JackTokenizer(source)
    engine = CompilationEngine(tokenizer)
    engine.compileClass()
    vm_path = jack_path.with_suffix('.vm')
    vm_path.write_text(engine.getOutput(), encoding='utf-8')
    print('  wrote ' + str(vm_path))


def main():
    if len(sys.argv) != 2:
        print('Usage: python JackCompiler.py <file.jack | directory>')
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        jack_files = sorted(target.glob('*.jack'))
        if not jack_files:
            print('no .jack files found in ' + str(target))
            sys.exit(1)
        for jf in jack_files:
            print('compiling ' + jf.name)
            compile_file(jf)

    elif target.is_file() and target.suffix == '.jack':
        print('compiling ' + target.name)
        compile_file(target)

    else:
        print('error: ' + str(target) + ' is not a .jack file or directory')
        sys.exit(1)

    print('done.')


if __name__ == '__main__':
    main()