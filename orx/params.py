import os

from orx.orx import Orx
import orx.parse
import util

class Parameters(Orx):
    """
    Class representing all of the data within the input parameters.
    """

    def __init__(self, homedir='.', filename=None, string=None):
        self.homedir = homedir
        self.defines = {}
        self.dests = []

        # get the actual data for this stuff
        if filename is not None:
            self.load_and_parse(filename)
        elif string is not None:
            self.single_line_parse(string)
        #print(self.dests)


    def exec_dest(self, args, kwargs):
        """
        Executes an orx parameters `dest` statement.
        """

        if 'structure' not in kwargs:
            raise ValueError("Missing structure value")
        if 'format' not in kwargs:
            raise ValueError("Missing format value(s)")
        if 'license' not in kwargs:
            raise ValueError("Missing license value(s)")
            # TODO: Just fall back to 'yes'

        for k, v in kwargs.items():
            if k == "format":
                for format in v.split(" "):
                    res = {}
                    
                    res["structure"] = kwargs["structure"]
                    res["format"] = format

                    if kwargs["license"] == "yes":
                        res["license"] = True
                    else:
                        res["license"] = False


                    self.dests.append(res)




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


    def single_line_parse(self, string):
        try:
            self.exec_expr(string)
        except Exception as e:
            raise Exception(f'In the given orx string, there was an error. {e}')
