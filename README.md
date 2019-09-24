![Orxporter logo with 'orxporter' next to it, in white against a lime green background.](orxporter_logo.png)
=========

Emoji exporter used for Mutant Standard emoji set

Introduction
------------

Orxporter is a tool for batch export operations for SVG-based emoji sets, providing multi-format and multi-resolution batch rendering, automated recolouring tools, unicode and shortcode filename export, JSON metadata export and more.


Disclaimer
----------

Orxporter was created as a rewrite of scripts used to automate some of the
workflow for Mutant Standard. Its main purpose remains to be the primary build
tool for Mutant Standard packages, and so its features are mainly focused on a
single use case.

That said, there has been interest in this tool, as it allows custom builds
or modifications of Mutant Standard packages, and is generic enough to work
for similar projects.

We welcome suggestions, feature requests and collaboration in order to make
orxporter more useful for independent emoji creators and end-users. We follow
Mutant Standard's code of conduct - please refer to **CODE_OF_CONDUCT.md**.


Features
--------

* Declarative language for defining semantics of emoji set
* Color mapping (recoloring)
* Outputting emoji both as shortcode-named files (ie. 'ice_cream') and unicode codepoint-named files (ie. '1f368').
* SVG, PNG, Lossless WebP and FLIF exports
* Supports multiple SVG renderers: rendersvg, inkscape and imagemagick
* Output options including emoji filtering, customisable export directory
  structure and filenaming
* JSON output of emoji set metadata
* Embedding licensing metadata for both PNG and SVG
* Multithreading

Prerequisites
-------------

* Python 3.6+
* A rasteriser if you are going to rasterise your SVGs:
    * [rendersvg](https://github.com/RazrFalcon/resvg/tree/master/tools/rendersvg) **(recommended rasteriser)**
    * Inkscape
    * ImageMagick
* exiftool (optional; for embedding licensing metadata)
* [FLIF](https://github.com/FLIF-hub/FLIF) (optional; for FLIF output)
* [libwebp](https://developers.google.com/speed/webp/docs/precompiled) (optional; for Lossless WebP output)

Usage
-----

By default, orxporter assumes the manifest is in **./manifest**, the input
directory is the **in** subdirectory of wherever the manifest is, and the
output directory is **out**. Default action is to export the entire emoji set
as shortcode-named SVG files.

Here are the command line options:

* **-h** -- prints the help message
* **-m PATH** -- specifies manifest file path (default: **manifest**)
* **-i PATH** -- specifies input image directory path; note that as build
  files are meant to be self-contained, this is relative to the manifest
  filepath (default: **in**)
* **-o PATH** -- specifies output directory path; this is relative to the
  current directory (default: **out**)
* **-f PATH_EXPR** -- specifies output filenaming for emoji; the following
  formatting codes are supported: **%c** for colormap, **%d** for source
  image's directory within input directory, **%f** for export format used,
  **%s** for shortcode, **%u** for unicode sequence, **%(property_name)** for
  emoji's property; (default: **%f/%s**)
* **-F FORMAT[,FORMAT...]** -- specifies output formats; the following
  formats are supported: **svg**, **png-SIZE** (fe. **png-64**); (default:
  **svg**)
* **-e FILTER** -- only emoji matching the filter condition will be exported;
  multiple filters can be used to narrow selection down but each requires a
  separate **-e** option; filters are specified as **property=val1[,val2...]**
  to match emoji with the property having the value (or one of listed values),
  __property=*__ to match emoji with the property being defined (regardless of
  value), or **property=!** to match emoji with the property being undefined
* **-j FILE** -- export emoji metadata to a JSON file
* **-J FILE** -- export emoji metadata to a JSON file in the format expected
  by Mutant Standard website code
* **-c** -- disable ANSI color codes; use if you see garbage in the terminal
  instead of pretty colorified output
* **-q WIDTHxHEIGHT** -- ensure source images have specified size
* **-t NUM** -- number of worker threads (default: **1**)
* **--force-desc** -- ensure all emoji have description (**desc** property)
* **-r RENDERER** -- selects rasteriser to use; the following rasterisers are
  supported: **inkscape**, **rendersvg**, **imagemagick**; **rendersvg** is
  recommended if speed is important; (default: **inkscape**)
* **-b NUM** -- maximum number of file arguments per exiftool call; larger
  numbers may accelerate metadata insertion but fail if the OS doesn't support
  sufficiently long argument lists; (default: **1000**)

Examples
--------

Export the entire emoji set as shortcode-named SVG files (default):
```
orxport.py
```

As above, but specifying manifest, input directory and output directory paths:

```
orxport.py -m <manifest file> -i <input directory> -o <output directory>
```

Export the entire emoji set as shortcode-named 64x64 and 256x256 PNG files,
with a separate directory for each format, using 4 threads:

```
orxport.py -F png-64,png-256 -f %f/%s -t 4
```

Export the entire emoji set as unicode-named SVG, 32x32 PNG, 128x128 PNG and
512x512 PNG files, using 8 threads, to a separate directory for each format,
ensuring that all input images are 32x32:

```
orxport.py -F svg,png-32,png-128,png-512 -f %f/%u -t 8 -q 32x32
```

Export only dark_elf emoji as a 256x256 PNG file:

```
orxport.py -F png-256 -e code=dark_elf
```

Export only emoji with v2 color modifier:

```
orxport.py -e color=v2
```

Export only paw emoji:

```
orxport.py -e morph=paw
```

Export all emoji as shortcode-named SVG files, preserving input directory
structure:

```
orxport.py -f %d/%s
```

Manifests
---------

Take a look at [*the manifest documentation**](docs/manifest.md) for more info.

Contributors
------------

* AndrewMontagne - imagemagick support
