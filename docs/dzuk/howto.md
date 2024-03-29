
# Main arguments

Orxporter's arguments are all marked by flags that can be positioned in any order.

eg.

```
./orxporter/orxport.py -m manifest/out.orx -i ../input -q 32x32 -o out/test_jxl -r resvg -f %f/%s -t 8 -C -F pngc-128,webp-128,jxl-128

```

Here are all of the arguments:


## Defining your emoji

### Manifest (`-m`)

Every emoji set in orxporter needs a Manifest. A Manifest file is one or a series of files (depending on how you split them up) that declare everything about your emoji sets - the emoji in them, what the emoji are, specifying colormaps for batch recolouring, categories for emoji pickers and what license metadata to use.

Manifests are written in a custom declarative language called orx.

I've written some guides on how this works, but until I finish them all, I recommend checking the [Mutant Standard build files](https://github.com/mutantstandard/build) to get an idea of how they work in practice.

- [How orx files work](../kiilas/manifest.md)
- Declaring emoji (TBA)
- Declaring and using colormaps (TBA)
- [How to use SVG and EXIF metadata in your manifest (optional)](metadata.md).


```
-m manifest.orx
```



## Input

### Input (`-i`)

The folder where the source images are located, the base directory at which all manifest `src` parameters start from.

```
-i input/folder/here
```

### Filter (`-e`) (optional)

Set a conditions for what emoji in your collection will actually get exported. Useful if you just want to export a slice of what you've got in your input and manifest.

Multiple filters can be used to narrow selection down but each requires a separate `-e` option.

Filter conditions run on data declared in your Manifest.

```
# only emoji from the category 'food_drink_herbs'
-e cat=food_drink_herbs

# only emoji from the categories 'food_drink_herbs' or 'symbols'.
-e cat=food_drink_herbs,symbols

# only emoji that don't have codepoints ('!' = undefined)
-e code=!

# only emoji that are in the 'food_drink_herbs' category AND don't have codepoints
-e cat=food_drink_herbs -e code=!

```



## Image output



### Output (`-o`)

Where forc outputs to a base level. Use the `-f` flag (mentioned below) for how to further organise outputs by generating directories.

```
-o /output/folder/here
```


### Directory and filename structure (`-f`) (optional)

This is a way of fiddling with the way that your output files are named and what folder structure they will be stored in.

[Check out this doc](file_structure.md) for the kinds of things you can do.





----------------------------------------------





## Image rendering and formats

### Formats (`-F`)

[Check out this doc](image_formats.md) for a list of the supported formats and how to type them.

You can put multiple formats in this flag in a comma-separated list like this:

````
-F svg,jxl-420,png-666,webp-128
````


### Renderer (`-r`) (optional)

This is how your SVGs will be rasterised. In the backend of Orxporter this means making PNGs, but this isn't just for PNG exports, but all other raster formats as they run a PNG in the export first, and then convert that PNG to the desired format. 

Depending on what you have installed on your computer, you can choose:

| software | flag in Orxporter | notes |
| :--    | :-- | :-- |
| [resvg](https://github.com/RazrFalcon/resvg) | (`-r resvg`) | I recommend this one if you don't have complicated SVG elements like filters. It's much faster than the others. |
| Inkscape | (`-r inkscape`) | Not recommended for macOS users. |
| ImageMagick  | (`-r imagemagick`) | |





----------------------------------------------





## Performance


### Cache (`-C`) (optional)

Set a directory as a cache. When a cache is set, Orxporter will store a keyed copy of all of your exported emoji there, so when you export again, Orxporter will only export the images that have changed or are in formats that it hasn't exported before, saving you a lot of time on repeat exports or publishing emoji set updates.

(Make sure you point to the same cache directory when re-exporting with a different command or script!)

```
-C cache/goes/here
```

### Threads (`-t`) (optional)

Run Orxporter's export operations into multiple concurrent threads. If you have a multi-threaded CPU (basically any CPU nowadays), it will greatly improve performance.

If you don't use this flag, Orxporter will only use 1 thread.


```
-t 8
```


-----

## Data output

Outputting metadata alongside the images can be really helpful for things like making emoji pickers and adding text descriptions into your applications.


### JSON export (`-j`/`-J`) (optional)

Compile the metadata you've set in .orx files into a JSON file for web and other applications.

Filters done with `-e` still apply to this export.

UsIf you use this flag, it will override any image-related flags, so if you want to export an image set and accompanying JSON, you have to do them in separate commands.

- `-j`: JSON file with a flat structure.
- `-J`: JSON with a specific format expected by the Mutant Standard website (and maybe yours too if you like!)


----


## Extra flags


### Force Text Descriptions (`--force-desc`)

Makes Orxporter complain if there are any emoji with missing text descriptions.


### Export without metadata embedding (`-l`) (optional)

If you have [specified metadata for embedding in your manifest](metadata.md), metadata
will be automatically embedded in compatible image outputs.
Using this flag will stop Orxporter from doing that.


### Check SVG image size (`-q`) (optional)

Check the size of your input SVGs' `viewBox` attribute to make sure there are no input emoji with the wrong size. This can be quite helpful if the way you make emoji can create little mistakes like this that can fall through in production.

This won't work if your input SVGs don't have a `viewBox` attribute.
