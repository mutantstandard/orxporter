
# Input (`-i`)`

The folder where the source images are located.

# Output (`-o`)

Where forc outputs to.

# [Manifest](manifest.md) (`-m`)

Where you set all of your emoji metadata.



# Filter (`-e`) (optional)

Set a conditions for what emoji in your input will actually get exported. Useful if you just want to export a slice of what you've got in your input and manifest.


----

# Image output

forc can export your stuff into two things: **images** and **data**.

These are all of the relevant commands for exporting images.

## [Formats](formats.md) (`-F`)

What image format(s) you want.

#### out of the box support:

- `svg` (SVG)
- `png` (PNG)

#### requires extra software to install:

- `webp` (Lossless WebP)
- `avif` (Lossless AVIF)
- `flif` (FLIF)

Check the 'Dependencies' part of the readme file to see which things you need to install to export to these formats.

When choosing raster images (any format but SVG), you have to add a size as well. you do this by adding a hyphen followed by the square size in pixels.

eg.

```
flif-32
avif-128
webp-512
png-60
```


## (`-f`)

## Renderer (`-r`) (optional)

This is how PNGs are produced (either standalone or for other formats like WebP and FLIF).
Depending on what you have or install, you can choose:
- inkscape
- imagemagick
- rendersvg

Based on our experiences, we highly recommend rendersvg because it is much faster than the others.
It's also much tidier to use on macOS.

## Check SVG image size (`-q`) (optional)

Check the size of your SVG's `viewBox` attribute to make sure there are no accidents in export.

This won't do anything if your SVGs don't have this attribute.

-----

# Data output

## JSON export (`-j`, `-J`) (optional)

Compile the metadata you've set in .orx files into a JSON file for web and other applications.

Filters done with `-e` still apply to this export.

Using this means that you're just exporting JSON for this command, you can't use the image-related stuff here.

- `-j`: JSON file with a flat structure.
- `-J`: JSON with a specific format expected by the Mutant Standard website (lol)

----

# Extra flags

## Force Text Descriptions

Makes forc complain if there are any emoji with missing text descriptions (e
