#!/usr/bin/env python3

import getopt
import os
import sys

import emoji
import export
import jsonutils
import log

import orx.manifest
import orx.params

VERSION = '0.3.0'

RENDERERS = ['inkscape', 'rendersvg', 'imagemagick']

DEF_INPUT = 'in'
DEF_MANIFEST = 'manifest.orx'
DEF_OUTPUT = 'out'

DEF_OUTPUT_NAMING = '%f/%s'
DEF_OUTPUT_FORMATS = ['svg']
DEF_LICENSE_ENABLED = True
DEF_PARAMS = 'parameters.orx'

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
-i      Input images (default: {DEF_INPUT})
-m      Manifest file (default: {DEF_MANIFEST})
-o      Output directory (default: {DEF_OUTPUT})


IMAGE BUILD:
----------------------------------------------------
-F      Format (default: {DEF_OUTPUT_FORMATS[0]})
        comma separated with no spaces (ie. 'svg,png-64,flif-128')
        - svg (SVG)
        - svgo (Optimised SVG, may have imperfect results)
        - png-SIZE (PNG)
        - pngc-SIZE (Crushed PNG)
        - flif-SIZE (FLIF)
        - webp-SIZE (Lossless WebP)
        - avif-SIZE (Lossless AVIF)

-f      Directory/filename naming system for output (default: {DEF_OUTPUT_NAMING})
        See the documentation for how this works.

-r      SVG renderer (default: {DEF_RENDERER})
        - rendersvg
        - imagemagick
        - inkscape

-l      Do not embed license metadata given in manifest

-p      Parameters file
        You can attach a parameters file instead of doing the 4 flags above.
        Adding this will overwrite anything entered in the previous 4 flags.

-t      Number of threads working on export tasks (default: {DEF_NUM_THREADS})


JSON BUILD:
----------------------------------------------------
-j <FILE>               export JSON replica of directory structure
-J <FILE>               export JSON metadata for mutstd website

Using JSON flags will override any image build flags.


OTHER OPTIONS:
----------------------------------------------------
-e <FILTER>             emoji filter
-q <WIDTHxHEIGHT>       ensure source images have certain size
-b <NUM>                maximum files per exiftool call (default: {DEF_MAX_BATCH})
--force-desc            ensure all emoji have a text description

TERMINAL OPTIONS:
----------------------------------------------------
-c                      disable ANSI color codes
--verbose               verbose printing
'''

def main():
    input_path = DEF_INPUT
    manifest_path = DEF_MANIFEST
    output_path = DEF_OUTPUT

    output_naming = DEF_OUTPUT_NAMING
    output_formats = DEF_OUTPUT_FORMATS
    renderer = DEF_RENDERER
    license_enabled = DEF_LICENSE_ENABLED
    params_path = None

    emoji_filter = []
    emoji_filter_text = "" # for error messaging only
    json_out = None
    json_web_out = None
    src_size = None
    num_threads = DEF_NUM_THREADS
    force_desc = False
    max_batch = DEF_MAX_BATCH
    verbose = False
    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hm:i:o:f:F:ce:j:J:q:t:r:b:p:l',
                                ['help', 'force-desc', 'verbose'])


        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print(HELP)
                sys.exit()

            # basics
            elif opt == '-m':
                manifest_path = arg
            elif opt == '-i':
                input_path = arg
            elif opt == '-o':
                output_path = arg

            # images
            elif opt == '-F':
                output_formats = arg.split(',')
            elif opt == '-f':
                output_naming = arg
            elif opt == '-r':
                renderer = arg
            elif opt == '-l':
                license_enabled = False
            elif opt == '-p':
                params_path = arg
            elif opt == '-t':
                num_threads = int(arg)
                if num_threads <= 0:
                    raise ValueError

            # JSON
            elif opt == '-j':
                json_out = arg
            elif opt == '-J':
                json_web_out = arg

            # other emoji stuff
            elif opt == '-e':
                k, v = arg.split('=')
                v = v.split(',')
                emoji_filter.append((k, v))
                emoji_filter_text = arg
            elif opt == '-q':
                t1, t2 = arg.split('x')
                src_size = int(t1), int(t2)
            elif opt == '-b':
                max_batch = int(arg)
                if max_batch <= 0:
                    raise ValueError
            elif opt == '--force-desc':
                force_desc = True

            # terminal stuff
            elif opt == '-c':
                log.use_color = False
            elif opt == '--verbose':
                verbose = True

    except Exception as e:
        log.out(f'x∆∆x {e}\n', 31)
        sys.exit(2)



# try to get all of the basic stuff and do the main execution
# -----------------------------------------------------------

    try:
        log.out(f'o∆∆o', 32) #hello


        # validate basic input that can't be checked while in progress
        if renderer not in RENDERERS:
            raise Exception(f"There's a mistake in your command arguments. '{renderer}' is not a renderer you can use in orxporter.")




        # create a Manifest
        # ie. parse the manifest file and get the information we need from it
        log.out(f'Loading manifest file...', 36)
        m = orx.manifest.Manifest(os.path.dirname(manifest_path),
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
        elif json_web_out:
            jsonutils.write_web(filtered_emoji, json_web_out)
        else:

            if params_path:
                log.out(f'Loading image export parameters...', 36)
                p = orx.params.Parameters(os.path.dirname(params_path),
                                      os.path.basename(params_path))
            else:
                # convert the non-parameter flags into an orx expression to be turned into a parameters object.
                log.out(f'Compiling image export parameters...', 36)
                license_text=""
                if license_enabled == True:
                    license_text = "yes"
                else:
                    license_text = "no"
                makeshift_params = f"dest  structure = {output_naming}   format = {' '.join(output_formats)}   license = {license_text}"
                p = orx.params.Parameters(string = makeshift_params)

            log.out(f'- {len(p.dests)} destination(s) defined.', 32)

            export.export(m, filtered_emoji, input_path, output_formats,
                          os.path.join(output_path, output_naming), src_size,
                          num_threads, renderer, max_batch, verbose, license_enabled)






    except (KeyboardInterrupt, SystemExit) as e:
        log.out(f'>∆∆< Cancelled!\n{e}', 93)
        sys.exit(1)

    # Where all the exceptions eventually go~
    except Exception as e:
        log.out(f'x∆∆x {e}\n', 31)
        raise e  # TEMP: for developer stuff
        sys.exit(1)

    # yay! finished!
    log.out('All done! ^∆∆^\n', 32) # goodbye

if __name__ == '__main__':
    main()
