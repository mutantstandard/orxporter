
import os
import pathlib
import subprocess

import svg
import image_proc

def to_svg(emoji_svg, out_path, license=None):
    """
    SVG exporting function. Doesn't create temporary files.
    Will append license <metadata> if requested.
    """
    if license:
        final_svg = svg.add_license(emoji_svg, license)
    else:
        final_svg = emoji_svg

    # write SVG out to file
    try:
        out = open(out_path, 'w')
        out.write(final_svg)
        out.close()
    except Exception as e:
        raise Exception(f'Could not write SVG to file: {e}')






def to_raster(emoji_svg, out_path, renderer, format, size, name):
    """
    Raster exporting function. Can export to any of orxporter's supported raster formats.
    Creates and deletes temporary SVG files. Might also create and delete temporary PNG files depending on the format.
    """
    tmp_svg_path = '.tmp' + name + '.svg'
    tmp_png_path = '.tmp' + name + '.png'

    # try to write a temporary SVG.
    image_proc.write_temp_svg(emoji_svg, tmp_svg_path)


    if format == "png":
        # single-step process
        image_proc.render_svg(tmp_svg_path, out_path, renderer, size)

    else:
        # multi-step process
        image_proc.render_svg(tmp_svg_path, tmp_png_path, renderer, size)

        if format == "webp":
            image_proc.convert_webp(tmp_png_path, out_path)
        elif format == "avif":
            image_proc.convert_avif(tmp_png_path, out_path)
        elif format == "flif":
            image_proc.convert_flif(tmp_png_path, out_path)
        else:
            os.remove(tmp_svg_path)
            os.remove(tmp_png_path)
            raise ValueError(f"This function wasn't given a correct format! ({format})")


    # delete temporary files
    os.remove(tmp_svg_path)

    if format != "png":
        os.remove(tmp_png_path)
