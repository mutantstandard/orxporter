# Formats

### Vector
- `svg` SVG

### Raster
- `png` PNG
- `pngc` Crushed PNG (requires oxipng)
- `webp` Lossless WebP (requires cwebp)
- `jxl` Lossless JPEG XL (requires [libjxl](https://github.com/libjxl/libjxl))

*(check the [readme](../../readme.md) for all the information on dependencies)*

When choosing raster images, you have to add a size as well. you do this by adding a hyphen followed by the square size in pixels.

eg.

```
jxl-64
webp-512
png-60
```

#### `pngc` Crushed PNG
Crushed PNG is the same format as PNG, but it's losslessly compressed to create a smaller file size. It requires an extra processing stage (which can be quite expensive on CPU at very large sizes like 512px), and it needs the dependency listed. Check the [oxipng](https://github.com/shssoichiro/oxipng) repo to see the documentation for it so you can see what it does to the PNG files.

Orxporter uses oxipng with the following command:

`oxipng <in file> --out, <out file> --quiet`

In tests with Mutant Standard emoji, Crushed PNGs have a file size reduction of between 40-70% (larger the reductions for larger file sizes), so if you're in a situation where you really need to care about file size, you should definitely use it over PNG.
