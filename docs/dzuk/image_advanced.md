# Slightly more advanced image output method

## Parameters (`-p`)

```
-p whoopdedoo.orx
```

This is the only thing you'll use for image input flags in this advanced method.

Parameters is an [orx file](orx.md), like the Manifest file, but it's a lot simpler.


```

dest
    structure = code_%f/%u
	format = pngc-32 pngc-128 pngc-512 webp-32 webp-128
    license = yes

dest
    structure = short_%f/%s
	format = pngc-32 pngc-128 pngc-512 webp-32 webp-128
    license = yes

dest
    structure = masto/ms_%s
	format = pngc-128
    license = yes

dest
    structure = font_sources/%f/ms_%s
	format = svg pngc-32 pngc-128
    license = no

```

- `dest` means 'destination'. It's essentially a bundle of export parameters. Every `dest` holds the same amount of info as a single simple image output command.
- `structure` is equivalent to an `-f` flag in simple exporting. It's where you declare the [file/folder structure](file_structure.md) of that destination.
- `format` is almost equivalent to an `-F` flag in simple exporting. It's where you define your [formats](image_formats.md). Unlike the `-F` flag, your formats should be separated by spaces instead of commas.
- `license` is equivalent to an `l` flag in simple exporting. You can choose whether this output destination will try to attach licensing metadata to the resulting files or not.

As you can see from the example above, using a Parameters file enables you to load more types of image export into a single orxporter command than you would be able to with the simple method.

If you're a heavy orxporter user, this method saves you time because orxporter doesn't execute each `dest` separately, so there are no wasted export/conversion tasks.
