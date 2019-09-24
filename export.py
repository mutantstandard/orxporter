import os
import queue
import time

from export_thread import ExportThread
from exception import FilterException
from paths import format_path, format_resolve
import log
import png
import svg




def export(m, filtered_emoji, input_path, formats, path, src_size,
           num_threads, renderer, max_batch):
    """
    Runs the entire export process, includes preliminary checking and validation
    of emoji metadata.
    """


    # verify emoji
    # --------------------------------------------------------------------------
    log.out('Checking emoji...', 36)
    for i, e in enumerate(filtered_emoji):

        code = e.get("code", "<UNNAMED>") # for possible info or error printouts

        try:
            format_path(path, e, 'svg')
        except FilterException as ex:
            #if str(ex):
            #    log.out(f'Skipping {code} - {ex}', 34, 4)
            #else:
            #    log.out(f'Skipping {code} (unknown reason)', 34)
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


    # export emoji
    # --------------------------------------------------------------------------
    log.out(f"Exporting emoji...", 36)

    if num_threads > 1:
        log.out(f"[{num_threads} threads]", 36)
    else:
        log.out(f"[{num_threads} thread]", 36)

    # start a Queue object for emoji export
    emoji_queue = queue.Queue()

    for entry in enumerate(filtered_emoji):
        emoji_queue.put(entry)

    # REMOVE: log.show_threads = num_threads > 1
    threads = []

    # initialise the amount of requested threads
    for i in range(num_threads):
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


    # waiting for threads to finish
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
        png.license(png_files, m.license.get('png'), max_batch)
