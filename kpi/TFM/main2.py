from lexer1 import Lexer
from parser import Parser


def main():
    f = 'file3.txt'
    L = Lexer(f)
    L.Analize()
    L.Display()
    if len(L.errorList) == 0:
        parser = Parser(L.lexemList, L.keywords, L.identifiers, L.delimiters, L.multiDelimiters, L.constants, L.errorList)
        parser.parse()


if __name__ == '__main__':
    main()
