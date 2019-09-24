import json
import os

import parse
import util

class Manifest:
    """
    Class representing all of the data within a manifest file.
    """

    def __init__(self, homedir='.', filename=None):
        self.homedir = homedir
        self.classes = {}
        self.colormaps = {}
        self.defines = {}
        self.emoji = []
        self.palettes = {}
        self.shortcodes = {}
        self.codepoints = {}
        self.license = {}
        if filename is not None:
            self.include(filename)


    def add_emoji(self, emoji):
        """
        Adds emoji to the manifest class. Will check for duplicate shortcodes
        and codepoints and will throw an error if there are any.
        """

        self.emoji.append(emoji)

        if 'code' in emoji:
            if emoji['code'] in self.shortcodes:
                raise ValueError('Shortcode already in use: ' + emoji['code'])
            self.shortcodes[emoji['code']] = emoji

        if 'unicode' in emoji and '!' not in emoji['unicode']:
            if emoji['unicode'] in self.codepoints:
                raise ValueError('Codepoint already in use: ' +
                                 util.uni_to_hex_hash(emoji['unicode']))
            self.codepoints[emoji['unicode']] = emoji


    def compile_emoji(self, kwargs, color=None):

        res = dict(kwargs)

        if not color and 'color' in res:
            del res['color']
        elif color:
            if color not in self.colormaps:
                raise ValueError('Undefined colormap: ' + color)
            res['color'] = color

        for k, v in res.items():
            if '%c' in v:
                if not color:
                    raise ValueError('%c without colormap')
                try:
                    res[k] = v.replace('%c', self.colormaps[color]['code'])
                except KeyError:
                    raise ValueError('Shortcode not defined for colormap: ' +
                                     color)
            if '%C' in v:
                if not color:
                    raise ValueError('%C without colormap')
                try:
                    subst = self.colormaps[color]['code']
                except KeyError:
                    raise ValueError('Shortcode not defined for colormap: ' +
                                     color)
                if subst:
                    subst = '_' + subst
                res[k] = v.replace('%C', subst)
            if '%u' in v:
                if not color:
                    raise ValueError('%u without colormap')
                try:
                    res[k] = v.replace('%u', self.colormaps[color]['unicode'])
                except KeyError:
                    raise ValueError('Codepoint not defined for colormap: ' +
                                     color)
            if '%U' in v:
                if not color:
                    raise ValueError('%U without colormap')
                try:
                    color_code = self.colormaps[color]['unicode']
                except KeyError:
                    raise ValueError('Codepoint not defined for colormap: ' +
                                     color)
                if color_code:
                    res[k] = v.replace('%U', '#200D ' + color_code)
                else:
                    res[k] = v.replace('%U', '')
            idx = 0
            while idx < len(v):
                idx = v.find('%(', idx)
                if idx == -1:
                    break
                end = v.find(')', idx+2)
                if end == -1:
                    raise ValueError('No matching parenthesis')
                prop = v[idx+2:end]
                if prop not in res:
                    raise ValueError('Undefined property: ' + prop)
                res[k] = v[:idx] + res[prop] + v[end+1:]
                idx += 1
                v = res[k]

        if 'unicode' in res:
            if '!' in res['unicode']:
                res['unicode'] = '!'
            else:
                unistr = []
                for char in res['unicode'].split():
                    try:
                        if char[0] == '#':
                            unistr.append(int(char[1:], 16))
                        else:
                            unistr.append(int(char))
                    except ValueError:
                        raise ValueError('Expected a number: ' + char)
                res['unicode'] = tuple(unistr)

        if 'desc' in res:
            if color:
                try:
                    color_desc = self.colormaps[color]['desc']
                except KeyError:
                    raise ValueError('Description not defined for colormap: ' +
                                     color)
                if color_desc:
                    res['desc'] += f' ({color_desc})'

        if 'root' not in res and not color and 'morph' not in res and 'code' in res:
            res['root'] = res['code']

        return res


    def exec_class(self, args, kwargs):
        if not args:
            raise ValueError('Missing id')
        if args[0] in self.classes:
            raise ValueError('Already defined: ' + args[0])
        if 'class' in kwargs:
            raise ValueError('Illegal recursion in class definition')

        res = {}

        for parent in args[1:]:
            if parent not in self.classes:
                raise ValueError('Parent class is undefined: ' + parent)
            res.update(self.classes[parent])
        res.update(kwargs)
        self.classes[args[0]] = res


    def exec_colormap(self, args, kwargs):
        if not args:
            raise ValueError('Missing id')
        if len(args) > 1:
            raise ValueError('Multiple ids')
        if args[0] in self.colormaps:
            raise ValueError('Already defined: ' + args[0])
        if 'src' not in kwargs:
            raise ValueError('Missing src')
        if 'dst' not in kwargs:
            raise ValueError('Missing dst')
        if kwargs['src'] not in self.palettes:
            raise ValueError('Undefined source palette: ' + kwargs['src'])
        if kwargs['dst'] not in self.palettes:
            raise ValueError('Undefined target palette: ' + kwargs['dst'])
        self.colormaps[args[0]] = kwargs


    def exec_define(self, args, kwargs):
        if kwargs:
            raise ValueError('kwargs not allowed in define expression')
        if len(args) < 2:
            raise ValueError('Missing argument')
        if args[0] in self.defines:
            raise ValueError('Already defined: ' + args[0])
        self.defines[args[0]] = ' '.join(args[1:])


    def exec_emoji(self, args, kwargs):
        emoji_args = {}
        for c in kwargs.get('class', '').split():
            if c not in self.classes:
                raise ValueError('Undefined class: ' + c)
            emoji_args.update(self.classes[c])
        emoji_args.update(kwargs)
        if 'src' not in emoji_args:
            raise ValueError('Missing src')
        if 'color' in emoji_args:
            for color in emoji_args['color'].split():
                self.add_emoji(self.compile_emoji(emoji_args, color))
        else:
            self.add_emoji(self.compile_emoji(emoji_args))


    def exec_include(self, args, kwargs):
        if not args:
            raise Exception('Missing filename')
        if len(args) > 1:
            raise ValueError('Multiple filenames')
        self.include(args[0])


    def exec_license(self, args, kwargs):
        for k, v in kwargs.items():
            path = os.path.join(self.homedir, v)
            if k == 'svg':
                try:
                    self.license['svg'] = open(path, 'r').read()
                except OSError:
                    raise Exception('Failed to load license file: ' + path)
            elif k == 'png':
                try:
                    self.license['png'] = json.load(open(path, 'r'))
                except OSError:
                    raise Exception('Failed to load license file: ' + path)
                except ValueError:
                    raise ValueError('Failed to parse JSON in file: ' + path)


    def exec_palette(self, args, kwargs):
        if not args:
            raise ValueError('Missing id')
        if len(args) > 1:
            raise ValueError('Multiple ids')
        if args[0] in self.palettes:
            raise ValueError('Already defined: ' + args[0])
        self.palettes[args[0]] = kwargs


    def exec_expr(self, expr):
        final_expr = parse.subst_consts(expr, self.defines)
        try:
            head, args, kwargs = parse.parse_expr(final_expr)
        except Exception:
            raise ValueError('Syntax error')
        if head is None:
            return
        elif head == 'class':
            self.exec_class(args, kwargs)
        elif head == 'colormap':
            self.exec_colormap(args, kwargs)
        elif head == 'define':
            self.exec_define(args, kwargs)
        elif head == 'emoji':
            self.exec_emoji(args, kwargs)
        elif head == 'include':
            self.exec_include(args, kwargs)
        elif head == 'license':
            self.exec_license(args, kwargs)
        elif head == 'palette':
            self.exec_palette(args, kwargs)
        else:
            raise ValueError('Unknown expression type: ' + head)


    def include(self, filename):
        try:
            m_file = open(os.path.join(self.homedir, filename), 'r')
        except OSError:
            raise Exception('Could not open manifest file: ' + filename)
        for expr, line_num in parse.exps(m_file):
            try:
                self.exec_expr(expr)
            except Exception as e:
                raise Exception(f'In manifest file `{filename}` at line '
                                f'{line_num}:\n'
                                f'`{expr.strip()}`\n'
                                f'Error: {e}')
        m_file.close()
