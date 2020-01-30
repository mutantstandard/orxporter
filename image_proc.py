import os
import pathlib
import subprocess



def write_temp_svg(emoji_svg, out_path):
    """
    Tries to write a temporary SVG out for exporting.
    """
    try:
        f = open(out_path, 'w')
        f.write(emoji_svg)
        f.close()

    except IOError:
        raise Exception('Could not write SVG to temporary file: ' + tmp_name)






def render_svg(svg_in, png_out, renderer, size):
    """
    Export a given SVG to a PNG based on the user's renderer choice.
    """

    if renderer == 'inkscape':
        cmd = ['inkscape', os.path.abspath(svg_in),
               '--export-png=' + os.path.abspath(png_out),
               '-h', str(size), '-w', str(size)]

    elif renderer == 'rendersvg':
        cmd = ['rendersvg', '-w', str(size), '-h', str(size),
                os.path.abspath(svg_in), os.path.abspath(png_out)]

    elif renderer == 'imagemagick':
        cmd = ['convert', '-background', 'none', '-density', str(size / 32 * 128),
               '-resize', str(size) + 'x' + str(size), os.path.abspath(svg_in), os.path.abspath(png_out)]
    else:
        raise AssertionError


    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode

    except Exception as e:
        raise Exception('Rasteriser invocation failed: ' + str(e))
    if r:
        raise Exception('Rasteriser returned error code: ' + str(r))







def convert_webp(png_in, webp_out):
    """
    Converts a PNG at `png_in` to a Lossless WebP at `webp_out`.

    Will raise an exception if trying to invoke the converter failed.
    """
    cmd_webp = ['cwebp', '-lossless', '-quiet', os.path.abspath(png_in), '-o', os.path.abspath(webp_out)]

    try:
        r = subprocess.run(cmd_webp, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('WebP converter invocation failed: ' + str(e))
    if r:
        raise Exception('WebP converter returned error code: ' + str(r))






def convert_avif(png_in, avif_out):
    """
    Converts a PNG at `png_in` to a Lossless AVIF at `avif_out`.

    Will raise an exception if trying to invoke the converter failed.
    """
    cmd_avif = ['avif', '-e', os.path.abspath(png_in), '-o', os.path.abspath(avif_out), '--lossless']

    try:
        r = subprocess.run(cmd_avif, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('AVIF converter invocation failed: ' + str(e))
    if r:
        raise Exception('AVIF converter returned error code: ' + str(r))




def convert_flif(png_in, flif_out):
    """
    Converts a PNG at `png_in` to a FLIF at `flif_out`.

    Will raise an exception if trying to invoke the converter failed.
    """
    cmd_flif = ['flif', '-e', '--overwrite', '-Q100', os.path.abspath(png_in), os.path.abspath(flif_out)]

    try:
        r = subprocess.run(cmd_flif, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('FLIF converter invocation failed: ' + str(e))
    if r:
        raise Exception('FLIF converter returned error code: ' + str(r))
