import os

from dest_paths import format_path, format_resolve
from exception import FilterException
import svg
import log

def emoji(m, filtered_emoji, input_path, formats, path, src_size,
           num_threads, renderer, max_batch, cache, verbose):
    """
    Checks all emoji in a very light validation as well as checking if emoji
    aren't filtered out by user choices.

    It only checks:
    - If the emoji has been filtered out by user exporting options.

    - If the source SVG file exists.
      (Will throw an Exception if not the case.)

    - If the shortcode ('short') attribute exists.
      (Will throw an Exception if not the case.)

    - If the svg size is consistent (if a -q flag is used).
      (Will throw an Exception if not the case.)

    It this doesn't result in an Exception, it returns dict containing
    a list of emoji that aren't filtered out, as well as a count
    of emoji that were skipped.
    """

    exporting_emoji = []
    cached_emoji = []
    partial_cached_emoji_count = 0
    skipped_emoji_count = 0

    for i, e in enumerate(filtered_emoji):

        short = e.get("short", "<UNNAMED>") # to provide info on possible error printouts

        try:
            format_path(path, e, 'svg')

        except FilterException as ex:
            if verbose:
                log.out(f"- - Skipped emoji: {short} - {ex}", 34)
            skipped_emoji_count += 1
            continue # skip if filtered out

        if 'src' not in e:
            raise ValueError(f"The emoji '{short}' is missing an 'src' attribute. It needs to have one.")



        # try to see if the source SVG file exists
        srcpath = os.path.join(m.homedir, input_path, e['src'])
        try:
            emoji_svg = open(srcpath, 'r').read()
        except Exception:
            raise ValueError(f"This source image for emoji '{short}' could not be loaded: {srcpath}")



        # the SVG size check (-q)
        if src_size is not None:
            img_size = svg.get_viewbox_size(emoji_svg)

            if img_size != src_size:
                raise ValueError("""The source image size for emoji '{}' is not what
                                was expected. It's supposed to be {}, but it's actually
                                {}.""".format(
                                    short,
                                    str(src_size[0]) + 'x' + str(src_size[1]),
                                    str(img_size[0]) + 'x' + str(img_size[1])
                                    ))

        if cache:
            # set the cache key in the emoji object for later reference
            emoji_cache_key = cache.get_cache_key(e, m, emoji_svg)
            e['cache_key'] = emoji_cache_key

            # check if the emoji is in cache
            cache_status = {f: cache.get_cache(e, f) for f in formats}
            cached_formats = [f for (f, p) in cache_status.items() if p]
            if len(cached_formats) == len(formats):
                cached_emoji.append(e)
            else:
                if cached_formats:
                    partial_cached_emoji_count += 1
                exporting_emoji.append(e)
        else:
            # add the emoji to exporting_emoji if it's passed all the tests.
            exporting_emoji.append(e)

    return { "exporting_emoji" : exporting_emoji
           , "skipped_emoji_count" : skipped_emoji_count
           , "cached_emoji": cached_emoji
           , "partial_cached_emoji_count": partial_cached_emoji_count
           }
