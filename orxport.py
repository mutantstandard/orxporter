#!/usr/bin/env python3

import getopt
import os
import sys

import emoji
import export
import jsonutils
import log
import manifest

VERSION = '0.2.1'

RENDERERS = ['inkscape', 'rendersvg', 'imagemagick']

DEF_MANIFEST = 'manifest'
DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_OUTPUT_NAMING = '%f/%s'
DEF_OUTPUT_FORMATS = ['svg']
DEF_NUM_THREADS = 1
DEF_RENDERER = 'inkscape'
DEF_MAX_BATCH = 1000

HELP = f'''orxporter {VERSION}
by Mutant Standard
(mutant.tech)

USAGE: orxport.py [options...]

HELP:
----------------------------------------------------
-h      Prints this help message.

Also look at /docs for full documentation.


INPUT:
----------------------------------------------------
-i      Input images (default: {DEF_INPUT_PATH})
-m      Manifest file (default: {DEF_MANIFEST})
-o      Output directory (default: {DEF_OUTPUT_PATH})


IMAGE BUILD:
----------------------------------------------------
-F      Format (default: {DEF_OUTPUT_FORMATS[0]})
        comma separated with no spaces (ie. 'SVGinOT,CBx,sbixOT')
        - svg
        - png-SIZE
        - flif-SIZE
        - webp-SIZE
        - avif-SIZE

-f      Directory/filename naming system for output (default: {DEF_OUTPUT_NAMING})
        See the documentation for how this works.

-t      Number of threads working on export tasks (default: {DEF_NUM_THREADS})

-r      SVG renderer (default: {DEF_RENDERER})
        - rendersvg
        - imagemagick
        - inkscape


JSON BUILD:
----------------------------------------------------
-j <FILE>               export JSON replica of directory structure
-J <FILE>               export JSON metadata for mutstd website


OTHER OPTIONS:
----------------------------------------------------
-e <FILTER>             emoji filter
-c                      disable ANSI color codes
-q <WIDTHxHEIGHT>       ensure source images have certain size
--force-desc            ensure all emoji have a text description
-b <NUM>                maximum files per exiftool call (default: {DEF_MAX_BATCH})
--verbose               verbose printing
'''

def main():
    manifest_path = DEF_MANIFEST
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    output_naming = DEF_OUTPUT_NAMING
    output_formats = DEF_OUTPUT_FORMATS
    emoji_filter = []
    emoji_filter_text = "" # for error messaging only
    json_out = None
    web_out = None
    src_size = None
    num_threads = DEF_NUM_THREADS
    force_desc = False
    renderer = DEF_RENDERER
    max_batch = DEF_MAX_BATCH
    verbose = False
    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hm:i:o:f:F:ce:j:J:q:t:r:b:',
                                ['help', 'force-desc', 'verbose'])
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print(HELP)
                sys.exit()
            elif opt == '-m':
                manifest_path = arg
            elif opt == '-i':
                input_path = arg
            elif opt == '-o':
                output_path = arg
            elif opt == '-f':
                output_naming = arg
            elif opt == '-F':
                output_formats = arg.split(',')
            elif opt == '-c':
                log.use_color = False
            elif opt == '-e':
                k, v = arg.split('=')
                v = v.split(',')
                emoji_filter.append((k, v))
                emoji_filter_text = arg
            elif opt == '-j':
                json_out = arg
            elif opt == '-J':
                web_out = arg
            elif opt == '-q':
                t1, t2 = arg.split('x')
                src_size = int(t1), int(t2)
            elif opt == '-t':
                num_threads = int(arg)
                if num_threads <= 0:
                    raise ValueError
            elif opt == '--force-desc':
                force_desc = True
            elif opt == '-r':
                renderer = arg
            elif opt == '-b':
                max_batch = int(arg)
                if max_batch <= 0:
                    raise ValueError
            elif opt == '--verbose':
                verbose = True
    except Exception:
        print(HELP)
        sys.exit(2)


    try:
        log.out(f'o∆∆o', 32) #hello

        # validate basic input that can't be checked while in progress
        if renderer not in RENDERERS:
            raise Exception(f"{renderer} is not a renderer you can use in orxporter.")

        # create a Manifest
        # ie. parse the manifest file and get the information we need from it
        log.out(f'Loading manifest file...', 36)
        m = manifest.Manifest(os.path.dirname(manifest_path),
                              os.path.basename(manifest_path))
        log.out(f'- {len(m.emoji)} emoji defined.', 32)

        # filter emoji (if any filter is present)
        filtered_emoji = [e for e in m.emoji if emoji.match(e, emoji_filter)]
        if emoji_filter:
            if filtered_emoji: # if more than 0
                log.out(f'- {len(filtered_emoji)} / {len(m.emoji)} emoji match the filter you gave.', 34)
            else:
                raise ValueError(f"Your filter ('{emoji_filter_text}') returned no results.")

        # ensure that descriptions are present if --force-desc flag is there
        if force_desc:
            nondesc = [e.get('code', str(e)) for e in filtered_emoji if 'desc' not in e]
            if nondesc:
                raise ValueError('You have emoji without a description: ' +
                                 ', '.join(nondesc))

        # JSON out or image out
        if json_out:
            jsonutils.write_emoji(filtered_emoji, json_out)
        elif web_out:
            jsonutils.write_web(filtered_emoji, web_out)
        else:
            export.export(m, filtered_emoji, input_path, output_formats,
                          os.path.join(output_path, output_naming), src_size,
                          num_threads, renderer, max_batch, verbose)

    except KeyboardInterrupt as e:
        log.out(f'\n>∆∆< Cancelled!\n{e}', 93)
        sys.exit(1)

    # Where all the exceptions eventually go~
    except Exception as e:
        log.out(f'x∆∆x {e}\n', 31)
        #raise e  ######################## TEMP, for developer stuff
        sys.exit(1)

    # yay! finished!
    log.out('All done! ^∆∆^\n', 32) # goodbye

if __name__ == '__main__':
    main()
