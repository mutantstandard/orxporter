# Usage


By default, orxporter assumes the manifest is in **./manifest**, the input
directory is the **in** subdirectory of wherever the manifest is, and the
output directory is **out**. Default action is to export the entire emoji set
as shortcode-named SVG files.

Here are the command line options:

- **-h** -- prints the help message
- **-m PATH** -- specifies manifest file path (default: **manifest**)
- **-i PATH** -- specifies input image directory path; note that as build
  files are meant to be self-contained, this is relative to the manifest
  filepath (default: **in**)
- **-o PATH** -- specifies output directory path; this is relative to the
- **-C PATH** -- (optional) specifies a cache path to save time on repeat exports
  current directory (default: **out**)
- **-f PATH_EXPR** -- specifies output filenaming for emoji; the following
  formatting codes are supported: **%c** for colormap, **%d** for source
  image's directory within input directory, **%f** for export format used, **%i**
  for image format without size, **%z** for image size without format (will return 0 for SVGs),
  **%s** for shortcode, **%u** for unicode sequence, **%(property_name)** for
  emoji's property; (default: **%f/%s**)
- **-F FORMAT[,FORMAT...]** -- specifies output formats; the following
  formats are supported: **svg**, **png-SIZE** (fe. **png-64**); (default:
  **svg**)
- **-e FILTER** -- only emoji matching the filter condition will be exported;
  multiple filters can be used to narrow selection down but each requires a
  separate **-e** option; filters are specified as **property=val1[,val2...]**
  to match emoji with the property having the value (or one of listed values),
  __property=*__ to match emoji with the property being defined (regardless of
  value), or **property=!** to match emoji with the property being undefined
- **-j FILE** -- export emoji metadata to a JSON file
- **-J FILE** -- export emoji metadata to a JSON file in the format expected
  by Mutant Standard website code
- **-c** -- disable ANSI color codes; use if you see garbage in the terminal
  instead of pretty colorified output
- **-q WIDTHxHEIGHT** -- ensure source images have specified size
- **-t NUM** -- number of worker threads (default: **1**)
- **--force-desc** -- ensure all emoji have description (**desc** property)
- **-r RENDERER** -- selects rasteriser to use; the following rasterisers are
  supported: **inkscape**, **rendersvg**, **imagemagick**; **rendersvg** is
  recommended if speed is important; (default: **inkscape**)
- **-b NUM** -- maximum number of file arguments per exiftool call; larger
  numbers may accelerate metadata insertion but fail if the OS doesn't support
  sufficiently long argument lists; (default: **1000**)

# Examples


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
orxport.py -F png-256 -e short=dark_elf
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

# Manifests


Take a look at [the manifest documentation](manifest.md) for more info.
