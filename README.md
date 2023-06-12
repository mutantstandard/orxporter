![Orxporter logo with 'Orxporter' next to it, in white against a lime green background.](orxporter_logo.png)

Orxporter is a rich toolkit for organising and exporting an SVG-based emoji set.
It has a system for storing emoji metadata and making large batch export operations
with that metadata.

---

# Features

- A [custom declarative language](docs/dzuk/orx.md) for defining your emoji semantics and metadata.
- Color remapping that automates the production of color-modifiable emoji.
- The ability to export emoji both as shortcode-named files (ie. 'ice_cream') and unicode codepoint-named files (ie. '1f368')
- Supports multiple SVG renderers (resvg, Inkscape and ImageMagick)
- Powerful output options including filtering, custom export directory structures and filename modifications.
- Optional cache system so you can save a lot of time on repeat exports.
- Multithreaded exports.
- Metadata embedding in your exports so you can embed things like licensing information into each emoji.
- Pretty terminal output and helpful error messages.


### Format Support
Orxporter is only designed to handle SVG image inputs, so you will need an SVG-based emoji set to use Orxporter.

Orxporter can export emoji sets to the following formats:

| Orxporter format code | format | license embedding |
| :--    | :--                                  | :--- |
| `svg`  | SVG                                  | SVG <metadata> |
| `png`  | PNG                                  | EXIF |
| `pngc` | Crushed PNG                          | EXIF |
| `webp` | Lossless WebP                        | not supported |
| `jxl`  | Lossless JPEG XL                     | not supported |

Certain compatible formats (noted above) can support SVG or EXIF metadata embedding.

You can also export your emoji set to fonts by using Orxporter in conjunction with [Forc](https://github.com/mutantstandard/forc). Forc has been designed to work seamlessly with Orxporter.



---

# Prerequisites

## Running orxporter
- Python 3.6+
- [progress](https://github.com/verigak/progress)

Install the compatible `progress` package by running the following in your shell:

```
pip install -r requirements.txt
```

## Making the images
Orxporter depends on other software to produce everything that's not SVG.

### SVG rasterisers
One SVG rasteriser is required for Orxporter to export to raster formats.

| software | purpose |
| :--    | :-- |
| [resvg](https://github.com/RazrFalcon/resvg) | (`-r resvg`). **We recommend this one if you don't have complicated SVG elements.** |
| Inkscape | (`-r inkscape`). Not recommended for macOS users. |
| ImageMagick  | (`-r imagemagick`). |


### Other format exporters
To export in certain formats, you will need other software installed:

| software | purpose |
| :--    | :-- |
| exiftool | Needed for EXIF metadata embedding |
| [oxipng](https://github.com/shssoichiro/oxipng) | Needed for Crushed PNG (`pngc`) output. |
| [webp](https://developers.google.com/speed/webp/docs/precompiled) | Needed for Lossless WebP (`webp`) output. |
| [libjxl](https://github.com/libjxl/libjxl) | Needed for Lossless JPEG XL (`jxl`) output. |



---------------------------------------------------

# How to use

There are two guides for using Orxporter:

### [Dzuk's how to guide](docs/dzuk/howto.md)

A detailed guide with simpler language for those who are less techincally inclined. It's not fully featured yet though.

### [kiilas's usage guide](docs/kiilas/usage.md)

The original guide, which is more concise and technical brief of how to use Orxporter. May not be up to date.



---

# Contributors and thanks

* @kiilas - Created the foundations of the program and the orx manifest language.
* @AndrewMontagne - imagemagick support
* @shello - caching, lots of fixes and stuff
* @dzuk-mutant - documentation, code cleanup, feature additions and changes

[Old changelog from 0.1.0 to 0.2.0](docs/old_changelog.md)

Thanks to the JPEG XL community with giving me some tips on adding encoder flags to improve output!

---

# Contributions

We welcome suggestions, feature requests and collaboration in order to make
Orxporter more useful for independent emoji creators and end-users. All contributors must follow
Mutant Standard's [code of conduct](docs/code_of_conduct.md).

---

# License

Orxporter is licensed under the [Cooperative Non-Violent License (CNPL) v4](license.txt).
