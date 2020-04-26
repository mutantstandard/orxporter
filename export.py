import itertools
import os
import queue
import time
import sys

import check
from exception import FilterException
from export_thread import ExportThread
from dest_paths import format_path, make_dir_structure_for_file
import image_proc
import log
from util import get_formats_for_license_type






def export(m, filtered_emoji, input_path, formats, path, src_size,
           num_threads, renderer, max_batch, verbose, license_enabled, cache):
    """
    Runs the entire orxporter process, includes preliminary checking and
    validation of emoji metadata and running the tasks associated with exporting.
    """

    # verify emoji (in a very basic way)
    # --------------------------------------------------------------------------
    log.out('Checking emoji...', 36)
    check_result = check.emoji(m, filtered_emoji, input_path, formats, path, src_size,
               num_threads, renderer, max_batch, cache, license_enabled, verbose)

    exporting_emoji = check_result["exporting_emoji"]
    cached_emoji = check_result["cached_emoji"]
    cached_emoji_count = check_result["cached_emoji_count"]
    skipped_emoji_count = check_result["skipped_emoji_count"]


    # report back how the export is going to go
    # --------------------------------------------------------------------------
    if skipped_emoji_count and verbose:
        log.out(f"", 34) # make a new line to break it up

    log.out(f"Output plan:", 34)

    if skipped_emoji_count:
        log.out(f"->[skip]    {skipped_emoji_count} emoji will be skipped.", 34)
        if not verbose:
            log.out(f"            (use the --verbose flag to see what those emoji are and why they are being skipped.)", 34)

    if cached_emoji_count:
        log.out(f"->[cache]   {cached_emoji_count} emoji will be reused from cache.", 34)
        if verbose:
            log.out(f"->[cache]      {len(cached_emoji['licensed_exports'])} licensed exports.", 34)
            log.out(f"->[cache]      {len(cached_emoji['exports'])} non-licensed exports.", 34)

    log.out(f"->[export]  {len(exporting_emoji)} emoji will be exported.", 34)


    # If there's no emoji to export, tell the program to quit.
    # --------------------------------------------------------------------------
    if len(exporting_emoji) == 0 and cached_emoji_count == 0:
        raise SystemExit('>∆∆< It looks like you have no emoji to export!')




    # export emoji
    # --------------------------------------------------------------------------
    # declare some specs of this export.

    if exporting_emoji:
        export_step(exporting_emoji, num_threads, m, input_path, path,
                    renderer, license_enabled, cache)



    # Copy files from cache
    # --------------------------------------------------------------------------
    if cached_emoji_count > 0:
        log.out(f"Copying {cached_emoji_count} emoji from cache...", 36)

        bar = log.get_progress_bar(max=cached_emoji_count)

        try:
            # Copy the exports (without license)
            for e, fs in cached_emoji['exports']:
                bar.next()
                for f in fs:
                    final_path = format_path(path, e, f)
                    make_dir_structure_for_file(final_path)
                    cache.load_from_cache(e, f, final_path, False)

            # Copy the licensed exports (populated if license_enabled is True)
            for e, fs in cached_emoji['licensed_exports']:
                bar.next()
                for f in fs:
                    final_path = format_path(path, e, f)
                    make_dir_structure_for_file(final_path)
                    cache.load_from_cache(e, f, final_path, True)
        except (KeyboardInterrupt, SystemExit):
            # Make sure the bar is properly set if oxporter is told to exit
            bar.finish()
            raise


        bar.finish()
        log.out(f"- done!", 32)


    # exif license pass
    # (currently only just applies to PNGs)
    # --------------------------------------------------------------------------
    if ('exif' in m.license) and license_enabled:
        exif_compatible_images = []
        exif_supported_formats = get_formats_for_license_type('exif')

        for e, fs in itertools.chain(exporting_emoji, cached_emoji['exports']):
            for f in fs:
                if f.split("-")[0] in exif_supported_formats:

                    try:
                        final_path = format_path(path, e, f)
                        exif_compatible_images.append((final_path, e, f))
                    except FilterException:
                        if verbose:
                            log.out(f"- Emoji filtered from metadata: {e['short']}", 34)
                        continue

        if exif_compatible_images:
            log.out(f'Adding EXIF metadata to all compatible raster files...', 36)
            images_list = (i for i, _, _ in exif_compatible_images)
            image_proc.batch_add_exif_metadata(images_list, m.license.get('exif'), max_batch)

            # Copy exported emoji to cache
            if cache:
                log.out(f"Copying {len(exif_compatible_images)} licensed "
                        "images to cache...", 36)
                for final_path, e, f in exif_compatible_images:
                    if not cache.save_to_cache(e, f, final_path, license_enabled=True):
                        raise RuntimeError(f"Unable to save '{e['short']}' in "
                                           f"{f} with license to cache.")



def export_step(exporting_emoji, num_threads, m, input_path, path, renderer, license_enabled, cache):
    log.out(f"Exporting {len(exporting_emoji)} emoji...", 36)

    if num_threads > 1:
        log.out(f"-> {num_threads} threads")
    else:
        log.out(f"-> {num_threads} thread")

    try:
        # start a Queue object for emoji export
        emoji_queue = queue.Queue()

        # put the [filtered] emoji+formats (plus the index, cuz enumerate()) into the queue.
        for entry in enumerate(exporting_emoji):
            emoji_queue.put(entry)

        # initialise the amount of requested threads
        threads = []
        for i in range(num_threads):
            threads.append(ExportThread(emoji_queue, str(i), len(exporting_emoji),
                                        m, input_path, path, renderer,
                                        license_enabled))


        # keeps checking if the export queue is done.
        bar = log.get_progress_bar(max=len(exporting_emoji))
        while True:
            done = emoji_queue.empty()

            bar.goto(log.export_task_count)

            # if the thread has an error, properly terminate it
            # and then raise an error.
            for t in threads:
                if t.err is not None:
                    for u in threads:
                        u.kill()
                        u.join()

                    raise ValueError(f'Thread {t.name} failed: {t.err}') from t.err

            if done:
                break

            time.sleep(0.01) # wait a little before seeing if stuff is done again.

        # finish the stuff
        # - join the threads
        # - then finish the terminal stuff
        for t in threads:
            t.join()


        bar.goto(log.export_task_count)
        bar.finish()


    except (KeyboardInterrupt, SystemExit):
        # make sure all those threads are tidied before exiting the program.
        # also make sure the bar is finished so it doesnt eat the cursor.
        bar.finish()
        log.out(f'Stopping threads and tidying up...', 93)
        if threads:
            for t in threads:
                t.kill()
                t.join()

        raise

    # Copy exported emoji to cache
    if cache:
        log.out(f'Copying {len(exporting_emoji)} exported emoji to '
                'cache...', 36)
        for emoji, fs in exporting_emoji:
            for f in fs:
                export_path = format_path(path, emoji, f)
                has_license = f in ('svg', 'svgo')
                if not cache.save_to_cache(emoji, f, export_path, has_license):
                    raise RuntimeError(f"Unable to save '{emoji['short']}' in "
                                       f"{f} to cache.")


    log.out('done!', 32)
    if log.filtered_export_task_count > 0:
        log.out(f"-> {log.filtered_export_task_count} emoji have been implicitly or explicitly filtered out of this export task.", 34)

    log.export_task_count = 0
    log.filtered_export_task_count = 0
