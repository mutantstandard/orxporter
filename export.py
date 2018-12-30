import os
import pathlib
import queue
import re
import subprocess
import threading
import time

import log
import png
import svg
import util



class ExportThread:
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
        if license:
            self.msg('* Writing license metadata...', indent=4)
            final_svg = svg.license(emoji_svg, license)
        else:
            final_svg = emoji_svg
        self.msg('* Exporting to file: ' + path, indent=4)
        try:
            out = open(path, 'w')
            out.write(final_svg)
            out.close()
        except Exception:
            raise Exception('Could not write to file: ' + path)



    def export_png(self, emoji_svg, size, path):
        self.msg('* Saving svg to temporary file...', indent=4)
        tmp_name = '.tmp' + self.name + '.svg'
        try:
            f = open(tmp_name, 'w')
            f.write(emoji_svg)
            f.close()
        except IOError:
            raise Exception('Could not write to temporary file: ' + tmp_name)
        self.msg(f'* Exporting at {size}px to {path}...', indent=4)
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
        self.msg('* Deleting temporary file...', indent=4)
        os.remove(tmp_name)




    def export_flif(self, emoji_svg, size, path):

        tmp_svg_name = '.tmp' + self.name + '.svg'
        tmp_png_name = '.tmp' + self.name + '.png'


        # try to write temporary SVG
        self.msg('* Saving svg to temporary file...', indent=4)

        try:
            f = open(tmp_svg_name, 'w')
            f.write(emoji_svg)
            f.close()

        except IOError:
            raise Exception('Could not write to temporary file: ' + tmp_svg_name)


        # build PNG export command based on renderer
        self.msg(f'* Exporting temporary png at {size}px', indent=4)

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


        # try to export temporary PNG
        try:
            r = subprocess.run(cmd_png, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('PNG rasteriser invocation failed: ' + str(e))
        if r:
            raise Exception('PNG rasteriser returned error code: ' + str(r))


        # try to export FLIF
        cmd_flif = ['flif', '-e', '-Q100', os.path.abspath(tmp_png_name), os.path.abspath(path)]


        try:
            r = subprocess.run(cmd_flif, stdout=subprocess.DEVNULL).returncode
        except Exception as e:
            raise Exception('FLIF converter invocation failed: ' + str(e))
        if r:
            raise Exception('FLIF converter returned error code: ' + str(r))



        # delete temporary files

        self.msg('* Deleting temporary files...', indent=4)
        os.remove(tmp_svg_name)
        os.remove(tmp_png_name)






    def export_webp(self, emoji_svg, size, path):

        tmp_svg_name = '.tmp' + self.name + '.svg'
        tmp_png_name = '.tmp' + self.name + '.png'


        # try to write temporary SVG
        self.msg('* Saving svg to temporary file...', indent=4)

        try:
            f = open(tmp_svg_name, 'w')
            f.write(emoji_svg)
            f.close()

        except IOError:
            raise Exception('Could not write to temporary file: ' + tmp_svg_name)


        # build PNG export command based on renderer
        self.msg(f'* Exporting temporary png at {size}px', indent=4)

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


        # try to export temporary PNG
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

        self.msg('* Deleting temporary files...', indent=4)
        os.remove(tmp_svg_name)
        os.remove(tmp_png_name)




    def export_emoji(self, emoji, emoji_svg, f, path, license):
        final_path = format_path(path, emoji, f)
        self.msg('* Export path is ' + final_path, indent=4)
        try:
            dirname = os.path.dirname(final_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
        except IOError:
            raise Exception('Could not create directory: ' + dirname)
        if f == 'svg':
            self.export_svg(emoji_svg, final_path, license.get('svg'))

        elif f.startswith('png-'):
            try:
                size = int(f[4:])
            except ValueError:
                raise ValueError('Invalid format: ' + f)
            self.export_png(emoji_svg, size, final_path)

        elif f.startswith('flif-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError('Invalid format: ' + f)
            self.export_flif(emoji_svg, size, final_path)

        elif f.startswith('webp-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError('Invalid format: ' + f)
            self.export_webp(emoji_svg, size, final_path)

        else:
            raise ValueError('Invalid format: ' + f)



    def run(self):
        try:
            while not self.kill_flag:
                try:
                    i, emoji = self.queue.get_nowait()
                except queue.Empty:
                    break
                self.msg(f'[{i+1} / {self.total}] Exporting '
                         f'{emoji.get("code", "<UNNAMED>")}...', 32)
                try:
                    format_path(self.path, emoji, 'svg')
                except SkipException as ex:
                    if str(ex):
                        self.msg(f'Skipping: {ex}', 34, 4)
                    else:
                        self.msg('Skipping', 34, 4)
                    continue
                if 'src' not in emoji:
                    raise ValueError('Missing src attribute')
                srcpath = os.path.join(self.m.homedir, self.input_path,
                                       emoji['src'])
                self.msg('* Loading source file: ' + srcpath, indent=4)
                try:
                    emoji_svg = open(srcpath, 'r').read()
                except Exception:
                    raise ValueError('Could not load file: ' + srcpath)
                if 'color' in emoji:
                    self.msg('* Converting colormap...', indent=4)
                    cmap = self.m.colormaps[emoji['color']]
                    pfrom = self.m.palettes[cmap['src']]
                    pto = self.m.palettes[cmap['dst']]
                    emoji_svg = svg.ctrans(emoji_svg, pfrom, pto)
                for f in self.formats:
                    self.msg('-> ' + f, 35)
                    self.export_emoji(emoji, emoji_svg, f, self.path, self.m.license)
        except Exception as e:
            self.err = e



class SkipException(Exception):
    def __init__(self, s=''):
        self.s = s

    def __str__(self):
        return self.s



def format_resolve(code, emoji, f):
    if code[0] == '(':
        inside = code[1:-1]
        if inside not in emoji:
            raise ValueError('Missing property: ' + inside)
        return emoji[inside]
    if code == 'c':
        if 'color' not in emoji:
            raise ValueError('Cannot resolve %c - no colormap')
        return emoji['color']
    if code == 'd':
        if 'src' not in emoji:
            raise ValueError('Cannot resolve %d - no emoji source file defined')
        return str(pathlib.Path(emoji['src']).parent)
    if code == 'f':
        return f
    if code == 's':
        if 'code' not in emoji:
            raise ValueError('Cannot resolve %s - no shortcode')
        return emoji['code']
    if code == 'u':
        if 'unicode' not in emoji:
            raise ValueError('Cannot resolve %u - no unicode codepoint defined')
        if '!' in emoji['unicode']:
            raise SkipException('Cannot resolve %u (explicitly undefined)')
        return util.uni_to_hex_filename(emoji['unicode'])
    raise ValueError('Cannot resolve format code: ' + code)



def format_path(path, emoji, f):
    res = path
    if f == 'svg':
        res = res + '.svg'
    elif f.startswith('png-'):
        res = res + '.png'
    elif f.startswith('flif-'):
        res = res + '.flif'
    elif f.startswith('webp-'):
        res = res + '.webp'
    else:
        raise ValueError('Invalid export format: ' + f)
    for match, fcode in set(re.findall(r'(%(\(.*\)|.))', res)):
        repl = format_resolve(fcode, emoji, f)
        res = res.replace(match, repl)
    return res



def export(m, filtered_emoji, input_path, formats, path, src_size,
           num_threads, renderer, max_batch):
    # 1st pass
    log.out('Performing sanity check...', 36)
    for i, e in enumerate(filtered_emoji):
        log.out(f'[{i+1} / {len(filtered_emoji)}] Checking '
                f'{e.get("code", "<UNNAMED>")}...', 32)
        try:
            format_path(path, e, 'svg')
        except SkipException as ex:
            if str(ex):
                log.out(f'Skipping: {ex})', 34, 4)
            else:
                log.out('Skipping', 34)
            continue
        if 'src' not in e:
            raise ValueError('Missing src attribute')
        srcpath = os.path.join(m.homedir, input_path, e['src'])
        try:
            emoji_svg = open(srcpath, 'r').read()
        except Exception:
            raise ValueError('Could not load file: ' + srcpath)
        if src_size is not None:
            imgsize = svg.size(emoji_svg)
            if imgsize != src_size:
                raise ValueError('Source image size is {}, expected {}'.format(
                    str(imgsize[0]) + 'x' + str(imgsize[1]),
                    str(src_size[0]) + 'x' + str(src_size[1])))
    # 2nd pass
    log.out('Exporting emoji...', 36)
    emoji_queue = queue.Queue()
    for entry in enumerate(filtered_emoji):
        emoji_queue.put(entry)
    log.show_threads = num_threads > 1
    threads = []
    for i in range(num_threads):
        log.out(f'Init thread {i}...', 35)
        threads.append(ExportThread(emoji_queue, str(i), len(filtered_emoji),
                                    m, input_path, formats, path, renderer))
    while True:
        done = emoji_queue.empty()
        for t in threads:
            if t.err is not None:
                for u in threads:
                    u.kill()
                    u.join()
                raise ValueError(f'Thread {t.name} failed: {t.err}')
        if done:
            break
        time.sleep(0.01)
    log.out(f'Waiting for all threads to finish...', 35)
    for t in threads:
        t.join()
    # png license pass
    if 'png' in m.license:
        png_files = []
        for e in filtered_emoji:
            for f in formats:
                if f.startswith('png-'):
                    try:
                        png_files.append(format_path(path, e, f))
                    except SkipException:
                        continue
        log.out(f'Adding license metadata to {len(png_files)} png files...', 36)
        png.license(png_files, m.license.get('png'), max_batch)
