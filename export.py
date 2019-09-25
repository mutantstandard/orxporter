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
           num_threads, renderer, max_batch):
    """
    Runs the entire orxporter process, includes preliminary checking and
    validation of emoji metadata and running the tasks associated with exporting.
    """


    # verify emoji
    # --------------------------------------------------------------------------
    log.out('Checking emoji...', 36)
    for i, e in enumerate(filtered_emoji):

        short = e.get("code", "<UNNAMED>") # to provide info on possible error printouts

        try:
            format_path(path, e, 'svg')
        except FilterException as ex:
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
                raise ValueError("The source image size for emoji '{}' is not what was expected. It's suppoed to be {}, but it's actually {}.".format(
                    short,
                    str(src_size[0]) + 'x' + str(src_size[1]),
                    str(imgsize[0]) + 'x' + str(imgsize[1])
                    ))

    log.out('done!', 33, 4)


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

    # start a Queue object for emoji export
    emoji_queue = queue.Queue()

    # put the [filtered] emoji (plus the index, cuz enumerate()) into the queue.
    for entry in enumerate(filtered_emoji):
        emoji_queue.put(entry)

    # initialise the amount of requested threads
    threads = []
    for i in range(num_threads):
        threads.append(ExportThread(emoji_queue, str(i), len(filtered_emoji),
                                    m, input_path, formats, path, renderer))


    # keeps checking if the export queue is done.
    log.bar.max = len(filtered_emoji)
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
    # - cleanup
    # - wait for threads to finish after they've all done their stuff.
    log.bar.finish()
    if log.filtered_export_task_count > 0:
        log.out(f"{log.filtered_export_task_count} emoji have been implicitly or explicitly filtered out of this export task.")


    log.export_task_count = 0
    log.filtered_export_task_count = 0

    for t in threads:
        t.join()



    # png license pass
    # --------------------------------------------------------------------------
    if 'png' in m.license:
        png_files = []
        for e in filtered_emoji:
            for f in formats:
                if f.startswith('png-'):
                    try:
                        png_files.append(format_path(path, e, f))
                    except FilterException:
                        continue

        log.out(f'Adding license metadata to png files...', 36)
        exif.add_license(png_files, m.license.get('png'), max_batch)
