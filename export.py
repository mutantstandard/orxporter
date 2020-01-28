import os
import queue
import time

from export_thread import ExportThread
from exception import FilterException
from paths import format_path, format_resolve
import log
import exif
import svg




def export(m, filtered_emoji, input_path, formats, path, src_size,
           num_threads, renderer, max_batch, verbose):
    """
    Runs the entire orxporter process, includes preliminary checking and
    validation of emoji metadata and running the tasks associated with exporting.
    """

    # verify emoji
    # --------------------------------------------------------------------------
    log.out('Checking emoji...', 36)


    exporting_emoji = []
    skipped_emoji_count = 0
    for i, e in enumerate(filtered_emoji):

        short = e.get("code", "<UNNAMED>") # to provide info on possible error printouts

        try:
            format_path(path, e, 'svg')
        except FilterException as ex:
            if verbose:
                log.out(f"- - Skipped emoji: {short} - {ex}", 34)
            skipped_emoji_count += 1
            continue #skip if filtered out

        if 'src' not in e:
            raise ValueError(f"The emoji '{short}' is missing an 'src' attribute. It needs to have one.")
        srcpath = os.path.join(m.homedir, input_path, e['src'])

        try:
            emoji_svg = open(srcpath, 'r').read()
        except Exception:
            raise ValueError(f"This source image for emoji '{short}' could not be loaded: {srcpath}")

        # the SVG size check (-q)
        if src_size is not None:
            imgsize = svg.get_viewbox_size(emoji_svg)
            if imgsize != src_size:
                raise ValueError("The source image size for emoji '{}' is not what was expected. It's supposed to be {}, but it's actually {}.".format(
                    short,
                    str(src_size[0]) + 'x' + str(src_size[1]),
                    str(imgsize[0]) + 'x' + str(imgsize[1])
                    ))

        # add the emoji to exporting_emoji if it's passed all the tests.
        exporting_emoji.append(e)

    if skipped_emoji_count > 0:
        log.out(f"- {skipped_emoji_count} emoji have been skipped, leaving {len(exporting_emoji)} emoji to export.", 34)

        if not verbose:
            log.out(f"- use the --verbose flag to see what those emoji are and why they were skipped.", 34)
    log.out('- done!', 32)




    # export emoji
    # --------------------------------------------------------------------------
    # declare some specs of this export.
    log.out("Exporting emoji...", 36)
    log.out(f"- {', '.join(formats)}")
    log.out(f"- to '{path}'")
    if num_threads > 1:
        log.out(f"- {num_threads} threads")
    else:
        log.out(f"- {num_threads} thread")

    try:
        # start a Queue object for emoji export
        emoji_queue = queue.Queue()

        # put the [filtered] emoji (plus the index, cuz enumerate()) into the queue.
        for entry in enumerate(exporting_emoji):
            emoji_queue.put(entry)

        # initialise the amount of requested threads
        threads = []
        for i in range(num_threads):
            threads.append(ExportThread(emoji_queue, str(i), len(exporting_emoji),
                                        m, input_path, formats, path, renderer))


        # keeps checking if the export queue is done.
        log.bar.max = len(exporting_emoji)
        while True:
            done = emoji_queue.empty()

            log.bar.goto(log.export_task_count)

            # if the thread has an error, properly terminate it
            # and then raise an error.
            for t in threads:
                if t.err is not None:
                    for u in threads:
                        u.kill()
                        u.join()
                    raise ValueError(f'Thread {t.name} failed: {t.err}')

            if done:
                break

            time.sleep(0.01) # wait a little before seeing if stuff is done again.

        # finish the stuff
        # - join the threads
        # - then finish the terminal stuff
        for t in threads:
            t.join()


        log.bar.goto(log.export_task_count)
        log.bar.finish()


    except (KeyboardInterrupt, SystemExit):
        # make sure all those threads are tidied before exiting the program.
        # also make sure the bar is finished so it doesnt eat the cursor.
        log.bar.finish()
        log.out(f'Stopping threads and tidying up...', 93)
        if threads:
            for t in threads:
                t.kill()
                t.join()

        raise


    log.out('- done!', 32)
    if log.filtered_export_task_count > 0:
        log.out(f"- {log.filtered_export_task_count} emoji have been implicitly or explicitly filtered out of this export task.", 34)

    log.export_task_count = 0
    log.filtered_export_task_count = 0




    # exif license pass
    # (currently only just applies to PNGs)
    # --------------------------------------------------------------------------
    if 'exif' in m.license:
        png_files = []
        for e in exporting_emoji:
            for f in formats:
                if f.startswith('png-'):
                    try:
                        png_files.append(format_path(path, e, f))
                    except FilterException:
                        if verbose:
                            log.out(f"- Filtered emoji: {e['short']}", 34)
                        continue
        if png_files:
            log.out(f'Adding license metadata to png files...', 36)
            exif.add_license(png_files, m.license.get('exif'), max_batch)
