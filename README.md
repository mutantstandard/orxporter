![Orxporter logo with 'orxporter' next to it, in white against a lime green background.](orxporter_logo.png)

Emoji exporter used for Mutant Standard emoji set

# Introduction

Orxporter is a tool for batch export operations for SVG-based emoji sets, providing multi-format and multi-resolution batch rendering, automated recolouring tools, unicode and shortcode filename export, JSON metadata export and more.


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


# Features


- Declarative language for defining semantics of emoji set
- Color mapping (recoloring)
- Outputting emoji both as shortcode-named files (ie. 'ice_cream') and unicode codepoint-named files (ie. '1f368').
- SVG, PNG, Lossless WebP, Lossless AVIF and FLIF exports
- Supports multiple SVG renderers: rendersvg, inkscape and imagemagick
- Output options including emoji filtering, customisable export directory
  structure and filenaming
- JSON output of emoji set metadata
- Embedding licensing metadata for both PNG and SVG
- Multithreading

# Prerequisites


- Python 3.6+
- [progress](https://github.com/verigak/progress)
- A rasteriser if you are going to rasterise your SVGs:
    - [rendersvg](https://github.com/RazrFalcon/resvg/tree/master/tools/rendersvg) **(recommended rasteriser)**
    - Inkscape
    - ImageMagick
- exiftool (optional; for embedding licensing metadata)
- [FLIF](https://github.com/FLIF-hub/FLIF) (optional; for FLIF output)
- [libwebp](https://developers.google.com/speed/webp/docs/precompiled) (optional; for Lossless WebP output)
- [go-avif](https://github.com/Kagami/go-avif) (optional; for AVIF output)


# How to use

There are two guides for using orxporter:

### [kiilas's usage guide](docs/kiilas/usage.md)

A more concise and technical brief of how to use orxporter.

### [Dzuk's how to guide](docs/dzuk/howto.md)

A longer guide with simpler language for those who are less techincally inclined. (Still requires that you know how CLIs and some other things work though)

# Contributors


* AndrewMontagne - imagemagick support
