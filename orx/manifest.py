import json
import os

from orx.orx import Orx
import orx.parse
import util

class Manifest(Orx):
    """
    Class representing all of the data within the input manifest.
    """

    def __init__(self, homedir='.', filename=None, string=None):
        self.homedir = homedir
        self.classes = {}
        self.colormaps = {}
        self.defines = {}
        self.emoji = []
        self.palettes = {}
        self.shortcodes = {}
        self.codepoints = {}
        self.license = {}

        # get the actual data for this stuff
        if filename is not None:
            self.load_and_parse(filename)


    def add_emoji(self, emoji):
        """
        Adds emoji to the manifest class. Will check for duplicate shortcodes
        and codepoints and will throw an error if there are any.
        """

        self.emoji.append(emoji)

        if 'short' in emoji:
            if emoji['short'] in self.shortcodes:
                raise ValueError('Shortcode already in use: ' + emoji['short'])
            self.shortcodes[emoji['short']] = emoji

        if 'code' in emoji and '!' not in emoji['code']:
            if emoji['code'] in self.codepoints:
                raise ValueError('Codepoint already in use: ' +
                                 util.uni_to_hex_hash(emoji['code']))
            self.codepoints[emoji['code']] = emoji


    def compile_emoji(self, kwargs, color=None):
        """
        Takes the basic output of `exec_emoji`, validates it, and returns a completed, compiled emoji object.

        kwargs: parameters from the manifest
        color: an attached colour for recolouring. (This is given by exec_emoji())
        """
        res = dict(kwargs)


        # if the input doesn't have colour, then the output doesnt
        if not color and 'color' in res:
            del res['color']
        elif color:
            # make sure whatever colour this emoji has is in the manifest.
            if color not in self.colormaps:
                raise ValueError('Undefined colormap: ' + color)
            res['color'] = color


        # formatting shortcode substitution
        # (for parameter values)
        #
        # this is performed first before other checks and stuff are performed to
        # the parameter contents.
        for k, v in res.items():

            # CM shortcode insertion (basic)
            if '%c' in v:
                if not color:
                    raise ValueError('%c without colormap')
                try:
                    res[k] = v.replace('%c', self.colormaps[color]['short'])
                except KeyError:
                    raise ValueError('Shortcode not defined for colormap: ' +
                                     color)

            # CM shortcode insertion (prepends and underscore if the shortcode isn't empty)
            if '%C' in v:
                if not color:
                    raise ValueError('%C without colormap')
                try:
                    subst = self.colormaps[color]['short']
                except KeyError:
                    raise ValueError('Shortcode not defined for colormap: ' +
                                     color)
                if subst:
                    subst = '_' + subst
                res[k] = v.replace('%C', subst)

            # CM codepoint insertion (basic)
            if '%u' in v:
                if not color:
                    raise ValueError('%u without colormap')
                try:
                    res[k] = v.replace('%u', self.colormaps[color]['code'])
                except KeyError:
                    raise ValueError('Codepoint not defined for colormap: ' +
                                     color)

            # CM codepoint insertion (prepend ZWJ if the shortcoode isn't empty)
            if '%U' in v:
                if not color:
                    raise ValueError('%U without colormap')
                try:
                    color_code = self.colormaps[color]['code']
                except KeyError:
                    raise ValueError('Codepoint not defined for colormap: ' +
                                     color)
                if color_code:
                    res[k] = v.replace('%U', '#200D ' + color_code)
                else:
                    res[k] = v.replace('%U', '')

            # param insertion
            # %(<param>)
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


        if 'code' in res:
            # it's either explicitly empty, or it's not
            if '!' in res['code']:
                res['code'] = '!'
            else:
                # attempt to interpret each part of the codepoint sequence as an int
                codeseq_list = []
                for codepoint in res['code'].split():
                    try:
                        if codepoint[0] == '#':
                            codeseq_list.append(int(codepoint[1:], 16))
                        else:
                            codeseq_list.append(int(codepoint))
                    except ValueError:
                        raise ValueError('Expected a number: ' + codepoint)
                res['code'] = tuple(codeseq_list)

        if 'desc' in res:
            # insert color modifier name at the end of the description.
            # ie. 'thumbs up (dark skin tone)'
            if color:
                try:
                    color_desc = self.colormaps[color]['desc']
                except KeyError:
                    raise ValueError('Description not defined for colormap: ' +
                                     color)
                if color_desc:
                    res['desc'] += f' ({color_desc})'

        if 'bundle' in res and color: 
            # replace the emoji bundle with the color bundle.
            res['bundle'] = self.colormaps[color]['bundle']
            

        # assume the shortcode is the same as the root if there are no modifiers going on.
        if 'root' not in res and not color and 'morph' not in res and 'short' in res:
            res['root'] = res['short']

        return res



    def exec_class(self, args, kwargs):
        """
        Executes an orx manifest `class` statement.
        """
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
        """
        Executes an orx manifest `colormap` statement.
        """
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



    def exec_emoji(self, args, kwargs):
        """
        Executes an orx manifest `emoji` statement.
        """
        emoji_args = {}

        for c in kwargs.get('class', '').split():
            if c not in self.classes:
                raise ValueError('Undefined class: ' + c)
            emoji_args.update(self.classes[c])
        emoji_args.update(kwargs)

        if 'src' not in emoji_args:
            raise ValueError('Missing src')

        # if the emoji has a 'color' parameter, duplicate it based on
        # the number of colourmaps are in that parameter, and attach
        # those colormaps to the dupes.
        if 'color' in emoji_args:
            for color in emoji_args['color'].split():
                self.add_emoji(self.compile_emoji(emoji_args, color))
        else:
            self.add_emoji(self.compile_emoji(emoji_args))




    def exec_license(self, args, kwargs):
        """
        Executes an orx manifest `license` statement.
        (Takes a license statement, verifies it and stores it in the manifest structure.)
        """
        for k, v in kwargs.items():
            path = os.path.join(self.homedir, v)

            # try to load the license files that were given.
            if k == 'svg':
                try:
                    self.license['svg'] = open(path, 'r').read()
                except OSError:
                    raise Exception('Failed to load license file: ' + path)
            elif k == 'exif':
                try:
                    self.license['exif'] = json.load(open(path, 'r'))
                except OSError:
                    raise Exception('Failed to load license file: ' + path)
                except ValueError:
                    raise ValueError('Failed to parse JSON in file: ' + path)



    def exec_palette(self, args, kwargs):
        """
        Executes an orx manifest `palette` statement.
        (Takes a palette statement, verifies it and stores it in the manifest structure.)
        """
        if not args:
            raise ValueError('Missing id')
        if len(args) > 1:
            raise ValueError('Multiple ids')
        if args[0] in self.palettes:
            raise ValueError('Already defined: ' + args[0])
        self.palettes[args[0]] = kwargs




    def exec_expr(self, expr):
        """
        Executes an orx manifest expression.
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
            self.exec_define(args, kwargs)
        elif head == 'include':
            self.exec_include(args, kwargs)

        elif head == 'class':
            self.exec_class(args, kwargs)
        elif head == 'colormap':
            self.exec_colormap(args, kwargs)
        elif head == 'emoji':
            self.exec_emoji(args, kwargs)
        elif head == 'license':
            self.exec_license(args, kwargs)
        elif head == 'palette':
            self.exec_palette(args, kwargs)
        else:
            raise ValueError('Unknown expression type: ' + head)
