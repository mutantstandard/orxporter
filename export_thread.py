import os
import pathlib
import queue
import subprocess
import threading

from exception import SkipException
from paths import format_path
import svg


class ExportThread:
    """
    A single thread handling exporting tasks.
    """
    def __init__(self, queue, name, total, m, input_path, formats, path,
                 renderer):
        self.queue = queue
        self.name = name
        self.total = total
        self.m = m
        self.input_path = input_path
        self.formats = formats
        self.path = path
        self.renderer = renderer
        self.err = None
        self.kill_flag = False
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def kill(self):
        self.kill_flag = True

    def join(self):
        self.thread.join()

    def msg(self, s, color=37, indent=0):
        log.out(s, color, indent, self.name)



    def export_svg(self, emoji_svg, path, license=None):
        """
        SVG exporting function
        """
        if license:
            final_svg = svg.license(emoji_svg, license)
        else:
            final_svg = emoji_svg

        # write SVG out to file
        try:
            out = open(path, 'w')
            out.write(final_svg)
            out.close()
        except Exception:
            raise Exception('Could not write to file: ' + path)

    def export_png(self, emoji_svg, size, path):

        # saving SVG to a temporary file
        tmp_name = '.tmp' + self.name + '.svg'
        try:
            f = open(tmp_name, 'w')
            f.write(emoji_svg)
            f.close()
        except IOError:
            raise Exception('Could not write to temporary file: ' + tmp_name)

        # export the SVG to a PNG based on the user's renderer
        if self.renderer == 'inkscape':
            cmd = ['inkscape', os.path.abspath(tmp_name),
                   '--export-png=' + os.path.abspath(path),
                   '-h', str(size), '-w', str(size)]
        elif self.renderer == 'rendersvg':
            cmd = ['rendersvg', '-w', str(size), '-h', str(size),
                    os.path.abspath(tmp_name), os.path.abspath(path)]
        elif self.renderer == 'imagemagick':
            cmd = ['convert', '-background', 'none', '-density', str(size / 32 * 128),
                   '-resize', str(size) + 'x' + str(size), os.path.abspath(tmp_name), os.path.abspath(path)]
        else:
            raise AssertionError
        try:
            r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('Rasteriser invocation failed: ' + str(e))
        if r:
            raise Exception('Rasteriser returned error code: ' + str(r))

        # delete temporary files
        os.remove(tmp_name)

    def export_flif(self, emoji_svg, size, path):
        """
        FLIF Exporting function. Creates temporary PNGs first before converting to WebP.
        """

        tmp_svg_name = '.tmp' + self.name + '.svg'
        tmp_png_name = '.tmp' + self.name + '.png'


        # try to write temporary SVG
        try:
            f = open(tmp_svg_name, 'w')
            f.write(emoji_svg)
            f.close()

        except IOError:
            raise Exception('Could not write to temporary file: ' + tmp_svg_name)


        # export the SVG to a temporary PNG based on the user's renderer
        if self.renderer == 'inkscape':
            cmd_png = ['inkscape', os.path.abspath(tmp_svg_name),
                   '--export-png=' + os.path.abspath(tmp_png_name),
                   '-h', str(size), '-w', str(size)]
        elif self.renderer == 'rendersvg':
            cmd_png = ['rendersvg', '-w', str(size), '-h', str(size),
                    os.path.abspath(tmp_svg_name), os.path.abspath(tmp_png_name)]
        elif self.renderer == 'imagemagick':
            cmd_png = ['convert', '-background', 'none', '-density', str(size / 32 * 128),
                   '-resize', str(size) + 'x' + str(size), os.path.abspath(tmp_svg_name), os.path.abspath(tmp_png_name)]
        else:
            raise AssertionError

        try:
            r = subprocess.run(cmd_png, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('PNG rasteriser invocation failed: ' + str(e))
        if r:
            raise Exception('PNG rasteriser returned error code: ' + str(r))


        # try to export FLIF
        cmd_flif = ['flif', '-e', '--overwrite', '-Q100', os.path.abspath(tmp_png_name), os.path.abspath(path)]

        try:
            r = subprocess.run(cmd_flif, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('FLIF converter invocation failed: ' + str(e))
        if r:
            raise Exception('FLIF converter returned error code: ' + str(r))



        # delete temporary files
        os.remove(tmp_svg_name)
        os.remove(tmp_png_name)

    def export_webp(self, emoji_svg, size, path):
        """
        WebP Exporting function. Creates temporary PNGs first before converting to WebP.
        """

        tmp_svg_name = '.tmp' + self.name + '.svg'
        tmp_png_name = '.tmp' + self.name + '.png'


        # try to write a temporary SVG
        try:
            f = open(tmp_svg_name, 'w')
            f.write(emoji_svg)
            f.close()

        except IOError:
            raise Exception('Could not write to temporary file: ' + tmp_svg_name)


        # export the SVG to a temporary PNG based on the user's renderer
        if self.renderer == 'inkscape':
            cmd_png = ['inkscape', os.path.abspath(tmp_svg_name),
                   '--export-png=' + os.path.abspath(tmp_png_name),
                   '-h', str(size), '-w', str(size)]
        elif self.renderer == 'rendersvg':
            cmd_png = ['rendersvg', '-w', str(size), '-h', str(size),
                    os.path.abspath(tmp_svg_name), os.path.abspath(tmp_png_name)]
        elif self.renderer == 'imagemagick':
            cmd_png = ['convert', '-background', 'none', '-density', str(size / 32 * 128),
                   '-resize', str(size) + 'x' + str(size), os.path.abspath(tmp_svg_name), os.path.abspath(tmp_png_name)]
        else:
            raise AssertionError


        try:
            r = subprocess.run(cmd_png, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('PNG rasteriser invocation failed: ' + str(e))
        if r:
            raise Exception('PNG rasteriser returned error code: ' + str(r))


        # try to export WebP
        cmd_webp = ['cwebp', '-lossless', os.path.abspath(tmp_png_name), '-o', os.path.abspath(path)]

        try:
            r = subprocess.run(cmd_webp, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('WebP converter invocation failed: ' + str(e))
        if r:
            raise Exception('WebP converter returned error code: ' + str(r))



        # delete temporary files
        os.remove(tmp_svg_name)
        os.remove(tmp_png_name)

    def export_emoji(self, emoji, emoji_svg, f, path, license):
        """
        Runs a single export batch.
        """
        final_path = format_path(path, emoji, f)

        # try to make the directory for this particular export batch.
        try:
            dirname = os.path.dirname(final_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
        except IOError:
            raise Exception('Could not create directory: ' + dirname)


        # run a format-specific export task on the emoji.
        if f == 'svg':
            self.export_svg(emoji_svg, final_path, license.get('svg'))

        elif f.startswith('png-'):
            try:
                size = int(f[4:])
            except ValueError:
                raise ValueError(f"The end ('{f[4:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            self.export_png(emoji_svg, size, final_path)

        elif f.startswith('flif-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError(f"The end ('{f[5:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            self.export_flif(emoji_svg, size, final_path)

        elif f.startswith('webp-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError(f"The end ('{f[5:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            self.export_webp(emoji_svg, size, final_path)

        else:
            raise ValueError('Invalid format: ' + f)



    def run(self):
        """
        The process of getting and executing a single export task in the queue.
        """
        try:
            while not self.kill_flag:

                # try to get an item from the queue.
                try:
                    i, emoji = self.queue.get_nowait()
                except queue.Empty:
                    break

                #self.msg(f'[{i+1} / {self.total}] Exporting '
                #         f'{emoji.get("code", "<UNNAMED>")}...', 32)
                try:
                    format_path(self.path, emoji, 'svg')
                except SkipException as ex:
                #    if str(ex):
                #        self.msg(f'Skipping: {ex}', 34, 4)
                #    else:
                #        self.msg('Skipping', 34, 4)
                    continue
                if 'src' not in emoji:
                    raise ValueError('Missing src attribute')
                srcpath = os.path.join(self.m.homedir, self.input_path,
                                       emoji['src'])

                # load the SVG source file
                try:
                    emoji_svg = open(srcpath, 'r').read()
                except Exception:
                    raise ValueError('Could not load file: ' + srcpath)

                # convert colormaps (if applicable)
                if 'color' in emoji:
                    cmap = self.m.colormaps[emoji['color']]
                    pfrom = self.m.palettes[cmap['src']]
                    pto = self.m.palettes[cmap['dst']]
                    emoji_svg = svg.ctrans(emoji_svg, pfrom, pto)

                # for each format in the emoji, export it as that
                for f in self.formats:
                    self.export_emoji(emoji, emoji_svg, f, self.path, self.m.license)

        except Exception as e:
            self.err = e
