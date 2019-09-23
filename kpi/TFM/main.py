from lexer import Lexer
from parser import Parser


def main():
    f = 'file1.txt'
    L = Lexer(f)
    L.Analize()
#     L.Display()
#     if len(L.errorList) == 0:
#         parser = Parser(L.lexemList, L.keywords, L.identifiers, L.delimiters, L.multiDelimiters, L.constants, L.errorList)
#         parser.parse()

# def True_Test():
#   for i in range(1,7):
#     f = 'file'+str(i)+'.txt'
#     L = Lexer(f)
#     L.Analize()
#     print ('True Test #{}'.format(i))
#     L.Display()

# def False_Test():
#   for i in range(7,12):
#     f = 'file'+str(i)+'.txt'
#     L = Lexer(f)
#     L.Analize()
#     print ('False Test #{}'.format(i))
#     L.Display()

if __name__ == '__main__':
    main()
