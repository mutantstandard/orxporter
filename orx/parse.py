"""
The module for parsing the basics of an orx file.

This just lifts the information from the syntax - this module is not responsible
for processing the actual data (that's where manifest comes in).
"""


def parse_expr(expr):
    """
    Parse Expression.

    Parses a single expression.
    """
    t1 = expr.split('=')
    t2 = list(map(lambda t: t.strip().rsplit(maxsplit=1), t1[:-1]))
    lex = (t2[0][0] if t2 else expr).split()
    head, args = (lex[0], lex[1:]) if lex else (None, [])
    keys = map(lambda t: t[1].strip(), t2)
    vals = list(map((lambda t: t[0].strip()), t2[1:])) + [t1[-1].strip()]
    for idx, val in enumerate(vals):
        if val == '!':
            vals[idx] = ''
    kwargs = dict(zip(keys, vals))
    return head, args, kwargs


def subst_consts(expr, consts):
    """
    Substitute Constants.

    Finds all of the constants from `define` expressions and fills
    in their actual value.

    parse_expr() takes the result of this function.
    """
    res = expr
    idx = 0
    while idx < len(res):
        idx = res.find('$', idx)
        if idx == -1:
            break
        if len(res) == idx + 1:
            raise ValueError('Missing constant name')
        if res[idx + 1] == '(':
            const_name_start = idx + 2
            const_name_end = res.find(')', idx + 2)
            const_token_end = const_name_end + 1
        else:
            const_name_start = idx + 1
            for const_name_end in range(idx + 1, len(res)):
                if res[const_name_end].isspace():
                    break
            else:
                const_name_end = len(res)
            const_token_end = const_name_end
        if const_name_end == -1:
            raise ValueError('Unterminated constant name')
        if const_name_start == const_name_end:
            raise ValueError('Missing constant name')
        const_name = res[const_name_start:const_name_end]
        if const_name not in consts:
            raise ValueError('Undefined constant: ' + const_name)
        res = res[:idx] + consts[const_name] + res[const_token_end:]
        idx += 1
    return res


def get_exprs(stream):
    """
    Get Expressions.

    An iterator that detects and retrieves single expressions.
    (whether they are single-line or multi-line expressions)
    """
    expr = ''
    expr_line_num = 1

    for line_num, line in enumerate(stream, 1):
        if not line:
            continue
        if line.lstrip().startswith('#'):
            continue
        if expr and not line[0].isspace():
            yield expr, expr_line_num
            expr = ''
        if not expr:
            expr_line_num = line_num
        expr += line

    if expr:
        yield expr, expr_line_num
        # expr: the expression itself.
        # expr_line_num: the line number where that expression is
        #    (for error messaging)
