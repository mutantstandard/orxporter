import os
import pathlib
import subprocess



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
    cmd = ['cwebp', '-lossless', '-quiet', os.path.abspath(png_in), '-o', os.path.abspath(webp_out)]

    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('Invoking the WebP converter (cwebp) failed: ' + str(e))
    if r:
        raise Exception('The WebP converter returned the following: ' + str(r))




def convert_avif(png_in, avif_out):
    """
    Converts a PNG at `png_in` to a Lossless AVIF at `avif_out`.
    Will raise an exception if trying to invoke the converter failed.
    """
    cmd = ['avif', '-e', os.path.abspath(png_in), '-o', os.path.abspath(avif_out), '--lossless']

    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('Invoking the AVIF converter (avif) failed: ' + str(e))
    if r:
        raise Exception('The AVIF converter returned the following: ' + str(r))




def convert_flif(png_in, flif_out):
    """
    Converts a PNG at `png_in` to a FLIF at `flif_out`.
    Will raise an exception if trying to invoke the converter failed.
    """
    cmd = ['flif', '-e', '--overwrite', '-Q100', os.path.abspath(png_in), os.path.abspath(flif_out)]

    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('Invoking the FLIF converter (flif) failed: ' + str(e))
    if r:
        raise Exception('The FLIF converter returned the following: ' + str(r))




def optimise_svg(svg_in, svgo_out):
    """
    Optimises an SVG at `svg_in` to `svgo_out`.
    Will raise an exception if trying to invoke the optimiser failed.
    """
    cmd = ['svgcleaner', os.path.abspath(svg_in), os.path.abspath(svgo_out), '--remove-metadata=no', '--quiet']

    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('Invoking the SVG optimiser (svgcleaner) failed: ' + str(e))
    if r:
        raise Exception('The SVG optimiser returned the following: ' + str(r))




def crush_png(png_in, pngc_out):
    """
    Crushes a PNG at `png_in` to `png_out`.
    Will raise an exception if trying to invoke the optimiser failed.
    """
    cmd = ['oxipng', os.path.abspath(png_in), '--out', os.path.abspath(pngc_out), '--quiet']

    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL).returncode
    except Exception as e:
        raise Exception('Invoking the PNG crusher (oxipng) failed: ' + str(e))
    if r:
        raise Exception('The PNG crusher returned the following: ' + str(r))
