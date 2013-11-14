#!/usr/bin/env python
import sys

from python_to_pythonjs import main as python_to_pythonjs
from pythonjs import main as pythonjs_to_javascript


def main(script):
    a = python_to_pythonjs(script)
    return pythonjs_to_javascript( a )


def command():
    scripts = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.endswith('.py'):
                scripts.append( arg )

    if len(scripts):
        a = []
        for script in scripts:
            a.append( open(script, 'rb').read() )
        data = '\n'.join( a )
    else:
        data = sys.stdin.read()

    js = main(data)
    print(js)


if __name__ == '__main__':
    command()
