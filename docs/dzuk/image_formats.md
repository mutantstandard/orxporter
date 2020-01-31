# Formats

### Vector
- `svg` SVG
- `svgo` Optimised SVG (requires svgcleaner)

*(check the [readme](../../readme.md) for all the information on dependencies)*

#### `svgo` Optimised SVG
Optimised SVG is the same format as SVG, but it's losslessly compressed to create a smaller file size (in Mutant Standard tests, optimised SVGs are 30-40% smaller). It requires an extra processing stage, and it needs the dependency listed. Check the [svgcleaner](https://github.com/RazrFalcon/svgcleaner) repo to see the documentation for it so you can see what it does to the SVG files.

orxporter uses svgcleaner with the following settings:

`svgcleaner <in file> <out file> --remove-metadata=no --quiet`


### Raster
- `png` PNG
- `webp` Lossless WebP (requires cwebp)
- `avif` Lossless AVIF (requires go-avif)
- `flif` FLIF (requires flif)

*(check the [readme](../../readme.md) for all the information on dependencies)*

When choosing raster images, you have to add a size as well. you do this by adding a hyphen followed by the square size in pixels.

eg.

```
flif-32
avif-128
webp-512
png-60
```
