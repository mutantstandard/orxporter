import os

from orx.orx import Orx
import orx.parse
import util

class Parameters(Orx):
    """
    Class representing all of the data within the input parameters.
    """

    def __init__(self, homedir='.', filename=None):
        self.dests = {}

        # get the actual data for this stuff
        if filename is not None:
            self.load_and_parse(filename)


    def exec_dest(self, args, kwargs):
        """
        Executes an orx parameters `dest` statement.
        """

        if not args:
            raise ValueError('Missing id')
        if args[0] in self.classes:
            raise ValueError('Already defined: ' + args[0])
        if 'class' in kwargs:
            raise ValueError('Illegal recursion in class definition')

        res = dict(kwargs)
        return res


    def exec_expr(self, expr):
        """
        Executes an orx parameters expression.
        """

        # finds all of the constants from `define` expressions and fills
        # in their actual value
        final_expr = orx.parse.subst_consts(expr, self.defines)


        # now parse all of the expressions
        #
        # head: the expression name ('emoji', 'define', 'color', etc.)
        # args: the arguments without parameters
        # kwargs: the arguments with parameters
        try:
            head, args, kwargs = orx.parse.parse_expr(final_expr)
        except Exception:
            raise ValueError('Syntax error')

        # execute each expression based on the head.
        # (or do nothing if there's no head)
        if head is None:
            return

        elif head == 'define':
            self.exec_include(args, kwargs)
        elif head == 'include':
            self.exec_include(args, kwargs)

        elif head == 'dest':
            self.exec_dest(args, kwargs)

        else:
            raise ValueError('Unknown expression type: ' + head)




    def load_and_parse(self, filename):
        """
        Loads and parses an orx parameters file.
        """

        # try to get the orx manifest file.
        try:
            m_file = open(os.path.join(self.homedir, filename), 'r')
        except OSError:
            raise Exception('Could not open parameters file: ' + filename)

        # parse the file.
        for expr, line_num in orx.parse.get_exprs(m_file):
            try:
                self.exec_expr(expr)
            except Exception as e:
                raise Exception(f'In manifest file `{filename}` at line '
                                f'{line_num}:\n'
                                f'`{expr.strip()}`\n'
                                f'Error: {e}')
        m_file.close()
