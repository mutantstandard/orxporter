
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







def to_png(emoji_svg, out_path, renderer, size, name):
    """
    PNG Exporting function. Creates temporary SVGs
    first before converting to PNG.
    """
    # saving SVG to a temporary file
    tmp_name = '.tmp' + name + '.svg'

    # try to write a temporary SVG.
    image_proc.write_temp_svg(emoji_svg, tmp_name)
    # try to render the SVG.
    image_proc.render_svg(tmp_name, out_path, renderer, size)

    # delete temporary files
    os.remove(tmp_name)







def to_webp(emoji_svg, out_path, renderer, size, name):
    """
    WebP Exporting function. Creates temporary SVGs and PNGs
    first before converting to WebP.
    """

    tmp_svg_path = '.tmp' + name + '.svg'
    tmp_png_path = '.tmp' + name + '.png'

    # try to write a temporary SVG.
    image_proc.write_temp_svg(emoji_svg, tmp_svg_path)
    # try to render the SVG.
    image_proc.render_svg(tmp_svg_path, tmp_png_path, renderer, size)
    # try to convert to WebP.
    image_proc.convert_webp(tmp_png_path, out_path)



    # delete temporary files
    os.remove(tmp_svg_path)
    os.remove(tmp_png_path)






def to_avif(emoji_svg, out_path, renderer, size, name):
    """
    Lossless AVIF Exporting function. Creates temporary SVGs and PNGs
    first before converting to AVIF.
    """

    tmp_svg_path = '.tmp' + name + '.svg'
    tmp_png_path = '.tmp' + name + '.png'


    # try to write a temporary SVG.
    image_proc.write_temp_svg(emoji_svg, tmp_svg_path)
    # try to render the SVG.
    image_proc.render_svg(tmp_svg_path, tmp_png_path, renderer, size)
    # try to convert to AVIF.
    image_proc.convert_avif(tmp_png_path, out_path)


    # delete temporary files
    os.remove(tmp_svg_path)
    os.remove(tmp_png_path)






def to_flif(emoji_svg, out_path, renderer, size, name):
    """
    FLIF Exporting function. Creates temporary SVGs and PNGs
    first before converting to FLIF.
    """

    tmp_svg_path = '.tmp' + name + '.svg'
    tmp_png_path = '.tmp' + name + '.png'

    # try to write a temporary SVG.
    image_proc.write_temp_svg(emoji_svg, tmp_svg_path)
    # try to render the SVG.
    image_proc.render_svg(tmp_svg_path, tmp_png_path, renderer, size)
    # try to convert to WebP.
    image_proc.convert_flif(tmp_png_path, out_path)



    # delete temporary files
    os.remove(tmp_svg_path)
    os.remove(tmp_png_path)
