
import os
import pathlib
import subprocess

import files
import svg
import image_proc

def to_svg(emoji_svg, out_path, name, license=None, include_license=True, optimise=False):
    """
    SVG exporting function. Doesn't create temporary files.
    Will append license <metadata> if requested.

    Can optimise the output (ie, output to svgo) if requested.
    """
    if include_license:
        final_svg = svg.add_license(emoji_svg, license)
    else:
        final_svg = emoji_svg

    # write SVG out to file
    if not optimise: # (svg)
        files.try_write(final_svg, out_path, "final SVG")
    else: # (svgo)
        tmp_svg_path = '.tmp' + name + '.svg'
        files.try_write(final_svg, tmp_svg_path, "temporary SVG")
        image_proc.optimise_svg(tmp_svg_path, out_path)
        os.remove(tmp_svg_path)




def to_raster(emoji_svg, out_path, renderer, format, size, name):
    """
    Raster exporting function. Can export to any of orxporter's supported raster formats.
    Creates and deletes temporary SVG files. Might also create and delete temporary PNG files depending on the format.
    """
    tmp_svg_path = '.tmp' + name + '.svg'
    tmp_png_path = '.tmp' + name + '.png'

    # try to write a temporary SVG.
    files.try_write(emoji_svg, tmp_svg_path, "temporary SVG")


    if format == "png":
        # one-step process
        image_proc.render_svg(tmp_svg_path, out_path, renderer, size)

    else:
        # two-step process
        image_proc.render_svg(tmp_svg_path, tmp_png_path, renderer, size)

        if format == "pngc":
            image_proc.crush_png(tmp_png_path, out_path)
        elif format == "webp":
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
