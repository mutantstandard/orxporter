
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

Set a directory as a cache. When a cache is set, orxporter will store a keyed copy of all of your exported emoji there, so when you export again, orxporter will only export the images that have changed or are in formats that it hasn't exported before, saving you time.

(Make sure you point to the same cache directory when re-exporting with a different command or script!)


### Output parameters

forc can export your stuff into two things: **images** and **data**. The parameters you use will differ.

----

#### Image output

There are two different methods to export images in orxporter:

##### [Simple method](image_easy.md)

For beginners and light users.

This method purely uses the command line to create exports.


##### [Slightly more advanced method](image_advanced.md)

For those who need to make heavy use of orxporter.

This method uses a .orx file to outline export types, enabling you to ask orxporter to compile more export types within a single go than you would be with command line arguments.


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

Makes orxporter complain if there are any emoji with missing text descriptions.


#### Check SVG image size (`-q`) (optional)

Check the size of your SVG's `viewBox` attribute to make sure there are no accidents in export.

This won't work if your SVGs don't have this attribute.
