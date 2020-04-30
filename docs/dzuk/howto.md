
### Input (`-i`)`

The folder where the source images are located.

### Output (`-o`)

Where forc outputs to.

### Manifest (`-m`)

A file where you set all of your emoji metadata.

Documentation on manifests coming soon.


### Filter (`-e`) (optional)

Set a conditions for what emoji in your input will actually get exported. Useful if you just want to export a slice of what you've got in your input and manifest.



### Cache (`-C`) (optional)

Set a directory as a cache. When a cache is set, Orxporter will store a keyed copy of all of your exported emoji there, so when you export again, Orxporter will only export the images that have changed or are in formats that it hasn't exported before, saving you time.

(Make sure you point to the same cache directory when re-exporting with a different command or script!)


### Output parameters

forc can export your stuff into two things: **images** and **data**. The parameters you use will differ.

----

#### Image output

##### Formats (`-F`)

[Check out this doc](image_formats.md) for a list of the supported formats and how to type them.

You can put multiple formats in this flag in a comma-separated list like this:

````
-F svg-69,flif-420,png-666,png-128
````

##### Directory and filename structure (`-f`) (optional)

This is a way of fiddling with the way that your output files are named and what folder structure they will be stored in.

[Check out this doc](file_structure.md) for the kinds of things you can do.


##### Renderer (`-r`) (optional)

This is how PNGs are produced (either standalone or for other formats like WebP and FLIF).
Depending on what you have installed on your computer, you can choose:

- `inkscape` (requires inkscape)
- `imagemagick` (requires ImageMagick)
- `rendersvg` (requires rendersvg)

*(check the [readme](../../readme.md) for all the information on dependencies)*

Based on our experiences, we highly recommend rendersvg (unless you need fancy SVG support like filters) because it is much faster than the others. (It's also much tidier to use on macOS.)



-----

#### Data output

##### JSON export (`-j`, `-J`) (optional)

Compile the metadata you've set in .orx files into a JSON file for web and other applications.

Filters done with `-e` still apply to this export.

Using this means that you're just exporting JSON for this command, you can't use the image-related stuff here.

- `-j`: JSON file with a flat structure.
- `-J`: JSON with a specific format expected by the Mutant Standard website (lol)

----

### [Metadata](metadata.md)

forc can embed SVG or EXIF metadata into your exported emoji sets.

---

### Extra flags

#### Force Text Descriptions (`--force-desc`)

Makes Orxporter complain if there are any emoji with missing text descriptions.


#### Check SVG image size (`-q`) (optional)

Check the size of your input SVGs' `viewBox` attribute to make sure there are no input emoji with the wrong size.

This won't work if your input SVGs don't have this attribute.
