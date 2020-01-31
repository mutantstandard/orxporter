# Formats

### Vector
- `svg` SVG
- `svgo` Optimised SVG (requires svgcleaner)

*(check the [readme](../../readme.md) for all the information on dependencies)*

#### `svgo` Optimised SVG
Optimised SVG is the same format as SVG, but it's losslessly compressed to create a smaller file size. It requires an extra processing stage (which is very cheap on CPU), and it needs the dependency listed. Check the [svgcleaner](https://github.com/RazrFalcon/svgcleaner) repo to see the documentation for it so you can see what it does to the SVG files.

orxporter uses svgcleaner with the following command:

`svgcleaner <in file> <out file> --remove-metadata=no --quiet`

In Mutant Standard tests, optimised SVGs are 30-40% smaller than normal SVGs.
However, svgcleaner is not perfect and can create some unexpected inconsistencies from the original version, so if you use this, you should check your input for flaws.


### Raster
- `png` PNG
- `pngc` Crushed PNG (requires oxipng)
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

#### `pngc` Crushed PNG
Crushed PNG is the same format as PNG, but it's losslessly compressed to create a smaller file size. It requires an extra processing stage (which can be quite expensive on CPU at very large sizes like 512px), and it needs the dependency listed. Check the [oxipng](https://github.com/shssoichiro/oxipng) repo to see the documentation for it so you can see what it does to the PNG files.

orxporter uses oxipng with the following command:

`oxipng <in file> --out, <out file> --quiet`

In Mutant Standard tests, Crushed PNGs have a file size reduction of about 25% compared to normal PNGs, but only on larger sizes (128px upwards). At 32px, crushing PNGs only has an average file size reduction of 3%.

Unlike Optimised SVGs, crushing PNGs is basically flawless in our experience.
