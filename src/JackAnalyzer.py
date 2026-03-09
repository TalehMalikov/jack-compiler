import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from JackTokenizer import JackTokenizer, tokenize_to_xml
from CompilationEngine import CompilationEngine


def analyze_file(jack_path):
    source = jack_path.read_text(encoding='utf-8')
    stem = jack_path.stem
    out_dir = jack_path.parent

    # write tokenizer output (XxxT.xml)
    token_xml = tokenize_to_xml(source)
    token_path = out_dir / (stem + 'T.xml')
    token_path.write_text(token_xml, encoding='utf-8')
    print('  wrote ' + str(token_path))

    # write parser output (Xxx.xml)
    tokenizer = JackTokenizer(source)
    engine = CompilationEngine(tokenizer)
    engine.compileClass()
    parse_path = out_dir / (stem + '.xml')
    parse_path.write_text(engine.getXML(), encoding='utf-8')
    print('  wrote ' + str(parse_path))


def main():
    if len(sys.argv) != 2:
        print('Usage: python JackAnalyzer.py <file.jack | directory>')
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_dir():
        jack_files = sorted(target.glob('*.jack'))
        if not jack_files:
            print('no .jack files found in ' + str(target))
            sys.exit(1)
        for jf in jack_files:
            print('analyzing ' + jf.name)
            analyze_file(jf)

    elif target.is_file() and target.suffix == '.jack':
        print('analyzing ' + target.name)
        analyze_file(target)

    else:
        print('error: ' + str(target) + ' is not a .jack file or directory')
        sys.exit(1)

    print('done.')


if __name__ == '__main__':
    main()