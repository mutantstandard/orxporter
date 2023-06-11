
# Main arguments

Orxporter's arguments are all marked by flags that can be positioned in any order.

eg.

```
./orxporter/orxport.py -m manifest/out.orx -i ../input -q 32x32 -o out/test_jxl -r resvg -f %f/%s -t 8 -C -F pngc-128,webp-128,jxl-128

```

Here are all of the arguments:



# Input

## Input (`-i`)

The folder where the source images are located.

```
-i input/folder/here
```

## Manifest (`-m`)

A file where you set all of your emoji metadata.

Documentation on manifests coming soon.

[How to use SVG and EXIF metadata in your manifest (optional)](metadata.md).


```
-m manifest.orx
```

## Filter (`-e`) (optional)

Set a conditions for what emoji in your collection will actually get exported. Useful if you just want to export a slice of what you've got in your input and manifest.

Multiple filters can be used to narrow selection down but each requires a separate `-e` option.

Filters are specified as:

```
property=val1[,val2...]**

```


  to match emoji with the property having the value (or one of listed values),
  __property=*__ to match emoji with the property being defined (regardless of
  value), or **property=!** to match emoji with the property being undefined

---

# Image output

The arguments and flags to use for image output:


## Output (`-o`)

Where forc outputs to a base level. Use the `-f` flag (mentioned below) for how to further organise outputs by generating directories.

```
-o /output/folder/here
```


## Directory and filename structure (`-f`) (optional)

This is a way of fiddling with the way that your output files are named and what folder structure they will be stored in.

[Check out this doc](file_structure.md) for the kinds of things you can do.


----


# Image rendering and formats

## Formats (`-F`)

[Check out this doc](image_formats.md) for a list of the supported formats and how to type them.

You can put multiple formats in this flag in a comma-separated list like this:

````
-F svg-69,flif-420,png-666,png-128
````


## Renderer (`-r`) (optional)

This is how your SVGs will be rasterised. In the backend of Orxporter this means making PNGs, but this isn't just for PNG exports, but all other raster formats as they run a PNG in the export first, and then convert that PNG to the desired format. 

Depending on what you have installed on your computer, you can choose:

- `inkscape` (requires inkscape)
- `imagemagick` (requires ImageMagick)
- `resvg` (requires resvg)

*(check the [readme](../readme.md) for all the information on dependencies)*

Based on our experiences, unless you need fancy SVG support like filters we highly recommend resvg because it is so much faster than the others.


----


# Performance


## Cache (`-C`) (optional)

Set a directory as a cache. When a cache is set, Orxporter will store a keyed copy of all of your exported emoji there, so when you export again, Orxporter will only export the images that have changed or are in formats that it hasn't exported before, saving you a lot of time on repeat exports or publishing emoji set updates.

(Make sure you point to the same cache directory when re-exporting with a different command or script!)

```
-C cache/goes/here
```

## Threads (`-t`) (optional)

Run export operations into multiple concurrent threads. If you have a multi-threaded CPU (basically any CPU nowadays), it will greatly improve performance.

If you don't use this flag, Orxporter will default to 1 thread.


-----

# Data output

The argument to use for JSON metadata output:

## JSON export (`-j`/`-J`) (optional)

Compile the metadata you've set in .orx files into a JSON file for web and other applications.

Filters done with `-e` still apply to this export.

Using this means that you're just exporting JSON for this command, you can't use the image-related stuff here.

- `-j`: JSON file with a flat structure.
- `-J`: JSON with a specific format expected by the Mutant Standard website (and maybe yours too if you like!)


----


# Extra flags


#### Force Text Descriptions (`--force-desc`)

Makes Orxporter complain if there are any emoji with missing text descriptions.


## Export without metadata embedding (`-l`) (optional)

If you have [specified metadata for embedding in your manifest](metadata.md), metadata
will be automatically embedded in compatible image outputs.
Using this flag will stop Orxporter from doing that.


#### Check SVG image size (`-q`) (optional)

Check the size of your input SVGs' `viewBox` attribute to make sure there are no input emoji with the wrong size. This can be quite helpful if the way you make emoji can create little mistakes like this that can fall through in production.

This won't work if your input SVGs don't have this attribute.
