import os
import pathlib
import queue
import subprocess
import threading

from exception import FilterException
import dest_paths
import export_task
import svg
import util
import log

class ExportThread:
    """
    A class representing and managing a single thread that executes
    exporting tasks from the export queue.
    """
    def __init__(self, queue, name, total, m, input_path, path,
                 renderer, license_enabled):
        self.queue = queue
        self.name = name
        self.total = total
        self.m = m
        self.input_path = input_path
        self.path = path
        self.renderer = renderer
        self.license_enabled = license_enabled
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


    def export_emoji(self, emoji, emoji_svg, f, path, license):
        """
        Runs a single export batch.
        """

        final_path = dest_paths.format_path(path, emoji, f)

        # try to make the directory for this particular export batch.
        dest_paths.make_dir_structure_for_file(final_path)


        # svg format doesn't involve a resolution so it can go straight to export.
        if f == 'svg':
            svg_license = license.get(util.get_license_type_for_format(f))
            export_task.to_svg(emoji_svg, final_path, self.name, svg_license, self.license_enabled, optimise=False)
        elif f == 'svgo':
            svg_license = license.get(util.get_license_type_for_format(f))
            export_task.to_svg(emoji_svg, final_path, self.name, svg_license, self.license_enabled, optimise=True)

        else:
            # any format other than svg is a raster, therefore it needs
            # to have a number separated by a dash.
            raster_format = f.split("-")
            try:
                size = int(raster_format[1])
            except ValueError:
                self.err = Exception(f"""A format you gave ('{f}') isn't correct. All formats
                                    that aren't svg must have a number separated by a dash.
                                    (ie 'png-32', 'webp-128')""")

            # now the size has been retrieved, try image
            # conversion based on the format.
            if raster_format[0] == "png":
                export_task.to_raster(emoji_svg, final_path, self.renderer, "png", size, self.name)

            elif raster_format[0] == "pngc":
                export_task.to_raster(emoji_svg, final_path, self.renderer, "pngc", size, self.name)

            elif raster_format[0] == "webp":
                export_task.to_raster(emoji_svg, final_path, self.renderer, "webp", size, self.name)

            elif raster_format[0] == "jxl":
                export_task.to_raster(emoji_svg, final_path, self.renderer, "jxl", size, self.name)

            elif raster_format[0] == "flif":
                export_task.to_raster(emoji_svg, final_path, self.renderer, "flif", size, self.name)

            elif raster_format[0] == "avif":
                export_task.to_raster(emoji_svg, final_path, self.renderer, "avif", size, self.name)

            else:
                self.err = Exception(f"""A format you gave ('{f}') uses a file format
                                ('{raster_format[0]}') that orxporter
                                doesn't support.""")



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
                # break the loop if nothing is left.
                try:
                    i, (emoji, formats) = self.queue.get_nowait()
                except queue.Empty:
                    break

                # compose the file path of the emoji.
                dest_paths.format_path(self.path, emoji, 'svg')

                # check if the src attribute is in the emoji.
                # if so, make a proper path out of it.
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
                    pfrom, pto = util.get_color_palettes(emoji, self.m)
                    emoji_svg = svg.translate_color(emoji_svg, pfrom, pto)

                # for each format in the emoji, export it as that
                for f in formats:
                    self.export_emoji(emoji, emoji_svg, f, self.path,
                                          self.m.license)

                # tell the progress bar that this task has been completed.
                log.export_task_count += 1

        except Exception as e:
            self.err = e
