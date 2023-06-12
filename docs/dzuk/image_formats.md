# Formats

## Vector
- `svg` SVG

## Raster
- `png` PNG
- `pngc` Crushed PNG
- `webp` Lossless WebP
- `jxl` Lossless JPEG XL

*(Most of these require that you install other software. Check the [readme](../../readme.md) for all the information on dependencies.)*

When choosing raster images, you have to add a size as well. you do this by adding a hyphen followed by the square size in pixels.

eg.

```
jxl-64
webp-512
png-60
```



## Some extra detail on formats


### `jxl` JPEG XL

JPEG XL is a recent format that is an extremely good, open, royalty-free format but is currently (as of June 2023) only supported on Apple platforms.

Orxporter currently uses the highest effort encoding `-e 9`, which does increase render times a bit but also does appreciably get file size down.


### `webp` WebP
WebP is the smallest file size you can get that enjoys wide browser support.

Orxpoorter uses default lossless settings as I've found this to have the best compression/conversion time ratio.

### `pngc` Crushed PNG
Crushed PNG is the same format as PNG, but it's losslessly compressed to create a smaller file size. It requires an extra processing stage (which can be quite expensive on CPU at very large sizes like 512px), and it needs the dependency listed. Check the [oxipng](https://github.com/shssoichiro/oxipng) repo to see the documentation for it so you can see what it does to the PNG files.

Orxporter uses oxipng with the following command:

`oxipng <in file> --out, <out file> --quiet`

In tests with Mutant Standard emoji, Crushed PNGs have a file size reduction of between 40-70% (larger the reductions for larger file sizes), so if you're in a situation where you really need to care about file size, you should definitely use it over PNG.
