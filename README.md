![Orxporter logo with 'orxporter' next to it, in white against a lime green background.](orxporter_logo.png)

orxporter is a rich toolkit for organising and exporting an SVG-based emoji set.
It has a system for storing emoji metadata and making large batch export operations
with that metadata, including multi-format and multi-resolution batch rendering,
automated recolouring tools, unicode and shortcode filename export, EXIF metadata
embedding, JSON metadata export and more.

---

# Features

- A custom declarative language for defining your emoji semantics and metadata
- Color remapping
- Outputting emoji both as shortcode-named files (ie. 'ice_cream') and unicode codepoint-named files (ie. '1f368')
- Export to SVG, PNG, Lossless WebP, Lossless AVIF and FLIF
- Optional lossless crushing of SVG and PNG files
- Supports multiple SVG renderers (rendersvg, Inkscape and ImageMagick)
- Output options including emoji filtering, export directory
  structure and filenames
- JSON output of emoji set metadata
- SVG and EXIF licensing metadata embedding
- Optional caching to save time on re-exporting
- Multithreading

---

# Prerequisites

- Python 3.6+
- [progress](https://github.com/verigak/progress)
- A rasteriser if you are going to rasterise your SVGs:
    - [rendersvg](https://github.com/RazrFalcon/resvg/tree/master/tools/rendersvg) **(recommended rasteriser)**
    - Inkscape
    - ImageMagick
- exiftool (Optional; for embedding EXIF license metadata)
- [svgcleaner](https://github.com/RazrFalcon/svgcleaner) (Optional; for Optimised SVG output)
- [oxipng](https://github.com/shssoichiro/oxipng) (Optional; for Crushed PNG output)
- [FLIF](https://github.com/FLIF-hub/FLIF) (Optional; for FLIF output)
- [libwebp](https://developers.google.com/speed/webp/docs/precompiled) (Optional; for Lossless WebP output)
- [go-avif](https://github.com/Kagami/go-avif) (Optional; for AVIF output) (Experimental; does not currently produce truly lossless images. We're trying to figure out why that is.)

Install the compatible `progress` package by running the following in your shell:

`pip install -r requirements.txt`

---

# How to use

There are two guides for using orxporter:

### [kiilas's usage guide](docs/kiilas/usage.md)

A more concise and technical brief of how to use orxporter.

### [Dzuk's how to guide](docs/dzuk/howto.md)

A longer guide with simpler language for those who are less techincally inclined. (Still requires that you know how CLIs and some other things work though)

---

# Contributors

* @AndrewMontagne - imagemagick support
* @shello - caching

[Old changelog from 0.1.0 to 0.2.0](docs/old_changelog.md)


---

# Disclaimer

Orxporter was created as a rewrite of scripts used to automate some of the
workflow for Mutant Standard. Its main purpose remains to be the primary build
tool for Mutant Standard packages, and so its features are mainly focused on a
single use case.

That said, there has been interest in this tool, as it allows custom builds
or modifications of Mutant Standard packages, and is generic enough to work
for similar projects.

We welcome suggestions, feature requests and collaboration in order to make
orxporter more useful for independent emoji creators and end-users. We follow
Mutant Standard's [code of conduct](docs/code_of_conduct.md).

---

# License

orxporter is licensed under the [Cooperative Non-Violent License (CNPL) v4](license.txt).
