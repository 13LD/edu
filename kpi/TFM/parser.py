from anytree import Node, RenderTree


class Parser:
    def __init__(self, lexem_string, keywords, identifiers, delimiters, multidelimiters, constant, errorList):
        self.lexem_iterator = lexem_string
        self.next_lexem = None
        self.keywords = keywords
        self.identifiers = identifiers
        self.delimiters = delimiters
        self.multidelimiters = multidelimiters
        self.constant = constant
        self.tree = Node('<signal-program>')
        self.i = -1
        if len(errorList) != 0:
            raise Exception

    def start_program(self):
        program = Node('<program>', parent=self.tree)
        next_lexem = self.get_next_lexem()
        if next_lexem.code != self.keywords['PROGRAM']:
            self.error(next_lexem, 'keyword PROGRAM')
        Node('{}   {}'.format(next_lexem.code, next_lexem.string), parent=program)

        next_lexem = self.get_next_lexem()
        if next_lexem.code not in self.identifiers.values():
            self.error(next_lexem, 'procedure identifier')
        Node('{}   {}'.format(next_lexem.code, next_lexem.string), (Node('<identifier>',  Node('<procedure-identifier>', parent=program))))

        self.semicolon(program)

        self.block(Node('<block>', parent=program))
        self.semicolon(program)

    def block(self, parent):
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code != self.keywords['BEGIN']:
            self.error(self.next_lexem, 'keyword BEGIN')
        Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=parent)

        self.statement_list(parent)

        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code != self.keywords['END']:
            self.error(self.next_lexem, 'keyword END')
        Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=parent)

    def statement_list(self, parent):
        stat_list = Node('<statements-list>', parent=parent)
        if self.statement(stat_list):
            self.statement_list(stat_list)
        else:
            self.i -= 1
            Node('<empty>', parent=stat_list)

    def statement(self, parent):
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code in self.constant.values():
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), ( Node('<unsigned-integer>', parent=statement)))
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code != self.delimiters[':']:
                self.error(self.next_lexem, 'colon')
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            if not self.statement(statement):
                self.error(self.next_lexem, 'statement')
            return 1

        if self.next_lexem.code in self.identifiers.values():
            statement = Node('<statement>', parent=parent)
            next_lexem = self.get_next_lexem()

            # variable-identifier
            if next_lexem.code == self.multidelimiters[':=']:
                Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), Node('<identifiers>', Node('<variable-identifiers>', parent=statement)))
                Node('{}   {}'.format(next_lexem.code, next_lexem.string), statement)
                self.unsigned_integer(statement)
                self.semicolon(statement)

            # procedure-identifier
            else:
                Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string),
                     Node('<identifiers>', Node('<procedure-identifiers>', parent=statement)))
                self.actual_arguments(statement, next_lexem)
                self.semicolon(statement)
            return 1

        if self.next_lexem.code == self.keywords['GOTO']:
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code not in self.constant.values():
                self.unsigned_integer(statement)
            else:
                self.i - 1     
            self.semicolon(statement)
            return 1

        if self.next_lexem.code == self.keywords['LINK']:
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.variable_identifier(statement)
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code != self.delimiters[',']:
                self.error(self.next_lexem, 'comma')
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), statement)
            self.unsigned_integer(statement)
            self.semicolon(statement)
            return 1

        if self.next_lexem.code == self.keywords['IN'] or self.next_lexem.code == self.keywords['OUT']:
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.unsigned_integer(statement)
            self.semicolon(statement)
            return 1

        if self.next_lexem.code == self.keywords['RETURN']:
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code != self.delimiters['(']:
                self.error(self.next_lexem, 'opening parenthesis')
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.statement_list(statement)
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code != self.delimiters[')']:
                self.error(self.next_lexem, 'closing parenthesis')
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.semicolon(statement)
            return 1

        if self.next_lexem.code == self.delimiters[';']:
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            return 1

        if self.next_lexem.code == self.multidelimiters['($']:
            statement = Node('<statement>', parent=parent)
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=statement)
            self.assembly_insert_file_identifier(statement)
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code != self.multidelimiters['$)']:
                self.error(self.next_lexem, '$)')
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), statement)
            return 1
        return 0

    def actual_arguments(self, parent, next_lexem):
        actual_arguments = Node('<actual-arguments>', parent)
        if next_lexem.code == self.delimiters['(']:
            Node('{}   {}'.format(next_lexem.code, next_lexem.string), actual_arguments)
            self.variable_identifier(actual_arguments)
            self.actual_arguments_list(actual_arguments)
            self.next_lexem = self.get_next_lexem()
            if self.next_lexem.code != self.delimiters[')']:
                self.error(self.next_lexem, 'closing parenthesis')
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), actual_arguments)
        else:
            self.i -=1
            Node('<empty>', actual_arguments)

    def actual_arguments_list(self,parent):
        actual_arguments_list = Node('<actual-arguments-list>', parent)
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code == self.delimiters[',']:
            Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), actual_arguments_list)
            self.variable_identifier(actual_arguments_list)
            self.actual_arguments_list(actual_arguments_list)
        else:
            self.i -= 1
            Node('<empty>', actual_arguments_list)

    def unsigned_integer(self, statement):
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code not in self.constant.values() or not self.next_lexem.code in self.next_lexem.code not in self.identifiers.values():
            self.error(self.next_lexem, 'unsigned integer')
        Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string),
             (Node('<unsigned-integer>', parent=statement)))

    def variable_identifier(self, parent):
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code not in self.identifiers.values():
            self.error(self.next_lexem, 'identifier')
        Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string),
             Node('<identifier>', Node('<variable-identifier>', parent=parent)))

    def assembly_insert_file_identifier(self, parent):
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code not in self.identifiers.values():
            self.error(self.next_lexem, 'identifier')
        Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string),
             Node('<identifier>', Node('<assembly-insert-file-identifier>', parent=parent)))


    def semicolon(self, parent):
        self.next_lexem = self.get_next_lexem()
        if self.next_lexem.code != self.delimiters[';']:
            self.error(self.next_lexem, 'semicolon')
        Node('{}   {}'.format(self.next_lexem.code, self.next_lexem.string), parent=parent)

    def parse(self):
        try:
            self.start_program()
            for pre, fill, node in RenderTree(self.tree):
                print("%s%s" % (pre, node.name))
        except Exception as e:
            for pre, fill, node in RenderTree(self.tree):
                print("%s%s" % (pre, node.name))
            print(e)

    def error(self, lexem, expected):
        raise Exception(
            'Unexpected token {} in line {}, column {}. Expected {}'.format(lexem.string,
                                                                                   lexem.row,
                                                                                   lexem.column, expected))

    def get_next_lexem(self):
        try:
            self.i += 1
            return self.lexem_iterator[self.i]
        except Exception as e:
            raise Exception('Unexpected end of file')




