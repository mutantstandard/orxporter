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
| `svgo` | Optimised SVG (Experimental; can change the appearance of certain SVG images)         | not supported |
| `png`  | PNG                                  | EXIF |
| `pngc` | Crushed PNG                          | EXIF |
| `webp` | Lossless WebP                        | not supported |
| `avif` | Lossless AVIF (Experimental; does not currently produce truly lossless images. We're trying to figure out why that is.) | not supported |
| `flif` | FLIF                                 | not supported |

Certain compatible formats (noted above) can support SVG or EXIF metadata embedding.

You can also export your emoji set to fonts by using Orxporter in conjunction with [Forc](https://github.com/mutantstandard/forc). Forc has been designed to work seamlessly with Orxporter.



---

# Prerequisites

## Main prerequisites
- Python 3.6+
- [progress](https://github.com/verigak/progress)

Install the compatible `progress` package by running the following in your shell:

```
pip install -r requirements.txt
```

## Image prerequisites
Orxporter depends on other software to produce most image export types.

### SVG rasterisers
One SVG rasteriser is required for Orxporter to export to raster formats (every other format other than `svg` and `svgo`):

| software | switch | notes
|----------|--------|-------
[resvg](https://github.com/RazrFalcon/resvg) | `-r resvg` | Recommended for speed. Available [on AUR, `resvg`](https://aur.archlinux.org/packages/resvg/).
Inkscape | `-r inkscape` | Not recommended for MacOS users.
ImageMagick  | `-r imagemagick`


### Other format exporters
To export in certain formats, you will need other software installed:

| software | purpose |
| :--    | :-- |
| exiftool | Needed for EXIF metadata embedding |
| [svgcleaner](https://github.com/RazrFalcon/svgcleaner) | Needed for Optimised SVG (`svgo`) output. |
| [oxipng](https://github.com/shssoichiro/oxipng) | Needed for Crushed PNG (`pngc`) output. |
| [webp](https://developers.google.com/speed/webp/docs/precompiled) | Needed for Lossless WebP (`webp`) output. |
| [FLIF](https://github.com/FLIF-hub/FLIF) | Needed for FLIF (`flif`) output. |
| [go-avif](https://github.com/Kagami/go-avif) | Needed for Lossless AVIF (`avif`) output. Requires `libaom`. (Experimental; does not currently produce truly lossless images. We're trying to figure out why that is.) |

Most of the above can be installed on macOS with [Homebrew](https://brew.sh/):

```
brew install exiftool svgcleaner oxipng webp flif
```

`go-avif` needs to be installed via `go get`, it requires libaom to work.

---

# How to use

There are two guides for using Orxporter:

### [Dzuk's how to guide](docs/dzuk/howto.md)

An up to date, detailed guide with simpler language for those who are less techincally inclined. (Still requires that you know how CLIs and some other things work though.)

### [kiilas's usage guide](docs/kiilas/usage.md)

The original guide, which is more concise and technical brief of how to use Orxporter. May not be up to date.



---

# Contributors

* @AndrewMontagne - imagemagick support
* @shello - caching, lots of fixes and stuff

[Old changelog from 0.1.0 to 0.2.0](docs/old_changelog.md)


---

# Contributions

We welcome suggestions, feature requests and collaboration in order to make
Orxporter more useful for independent emoji creators and end-users. All contributors must follow
Mutant Standard's [code of conduct](docs/code_of_conduct.md).

---

# License

Orxporter is licensed under the [Cooperative Non-Violent License (CNPL) v4](license.txt).
