import json
import os

import orx.parse
import util


class Orx:
    """
    Class that represents the basics of an orx file.
    """

    def __init__(self, homedir='.', filename=None):
        self.homedir = homedir
        self.defines = {}

        # get the actual data for this stuff
        if filename is not None:
            self.load_and_parse(filename)


    def exec_define(self, args, kwargs):
        """
        Executes an orx manifest `define` statement.
        """
        if kwargs:
            raise ValueError('kwargs not allowed in define expression')
        if len(args) < 2:
            raise ValueError('Missing argument')
        if args[0] in self.defines:
            raise ValueError('Already defined: ' + args[0])
        self.defines[args[0]] = ' '.join(args[1:])


    def exec_include(self, args, kwargs):
        """
        Executes an orx manifest `include` statement.
        """
        if not args:
            raise Exception('Missing filename')
        if len(args) > 1:
            raise ValueError('Multiple filenames')
        self.load_and_parse(args[0])


    def load_and_parse(self, filename):
        """
        Loads and parses an orx manifest file.
        """

        # try to get the orx manifest file.
        try:
            m_file = open(os.path.join(self.homedir, filename), 'r')
        except OSError:
            raise Exception('Could not open manifest file: ' + filename)

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
