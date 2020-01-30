import os
import pathlib
import queue
import subprocess
import threading

from exception import FilterException
from dest_paths import format_path
import export_task
import svg
import log

class ExportThread:
    """
    A class representing and managing a single thread that executes
    exporting tasks from the export queue.
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
        # this essentially tells self.run() to stop running if it is True
        self.kill_flag = False
        # the actual thread part of this thread
        self.thread = threading.Thread(target=self.run)


        # start the thread part of this thread!
        self.thread.start()


    def kill(self):
        """
        Requests this thread to be teriminated by activating the self.kill_flag flag.
        (This effectively stops self.run() from running)
        """
        self.kill_flag = True

    def join(self):
        """
        Wait for this thread to finish and merge it.
        """
        self.thread.join()

    def msg(self, s, color=37, indent=0):
        log.out(s, color, indent, self.name)




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
            export_task.to_svg(emoji_svg, final_path, license.get('svg'))

        elif f.startswith('png-'):
            try:
                size = int(f[4:])
            except ValueError:
                raise ValueError(f"The end ('{f[4:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            export_task.to_png(emoji_svg, final_path, self.renderer, size, self.name)

        elif f.startswith('flif-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError(f"The end ('{f[5:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            export_task.to_flif(emoji_svg, final_path, self.renderer, size, self.name)

        elif f.startswith('webp-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError(f"The end ('{f[5:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            export_task.to_webp(emoji_svg, final_path, self.renderer, size, self.name)


        elif f.startswith('avif-'):
            try:
                size = int(f[5:])
            except ValueError:
                raise ValueError(f"The end ('{f[5:]}') of a format you gave ('{f}') isn't a number. It must be a number.")
            export_task.to_avif(emoji_svg, final_path, self.renderer, size, self.name)

        else:
            raise ValueError('Invalid format: ' + f)



    def run(self):
        """
        The process of getting and executing a single export task in
        the queue.

        This is what the actual thread part of this class is tasked
        with working on.
        """
        try:
            # basically: do stuff as long as it's not requested to
            # be killed by the class
            while not self.kill_flag:

                # try to get an item from the queue.
                try:
                    i, emoji = self.queue.get_nowait()
                except queue.Empty:
                    break

                # compose the file path of the emoji.
                format_path(self.path, emoji, 'svg')

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
                    emoji_svg = svg.translate_color(emoji_svg, pfrom, pto)

                # for each format in the emoji, export it as that
                for f in self.formats:
                    self.export_emoji(emoji, emoji_svg, f, self.path, self.m.license)

                # tell the progress bar that this task has been completed.
                log.export_task_count += 1

        except Exception as e:
            self.err = e
