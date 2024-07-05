
# File structure formatting

Orxporter lets you use various points of data to format your emoji image output.

In this, you denote (in UNIX style, basically, with forward slashes ('/') instead of Windows' backslashes ('\\') ) the path relative to your chosen output folder to where your emoji are.

You can use any of these for filenames as well as folders, but it's generally recommended to only use `%u` or `%s` for filenames.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg

# out folder
# (flag -o or parameter 'out')
final

# file structure formatting
# (flag -f or parameter 'structure')
%f/%s

# output (assuming it's a PNG at 32px)
final/png-32/hand.png

```

So as you can see here, your full export path for any emoji is a combination of what your out folder is, what this is.

This feature is essentially optional; if you don't use this feature for your output, it will default to '%f/%s' (what's shown in the example above).

As I'll explain in this file, it's a pretty powerful way of providing different structures and emoji names based on this project. This is also how you can choose between shortcode and codepoint filenames.

If you include a property that is optional, like `code` (via `%u`), or `cat` (via `%(cat)`), it essentially acts as a filter; it will make this export will skip those that do not have those features.

---

## Colormap (`%c`)

Inserts the name of the emoji's colormap at the time of export.

Keep in mind that at export time, Orxporter duplicates an emoji with multiple colormap into individualised versions with each colour. So if an emoji has multiple colors, this expression will expand into as many colours it's been assigned.

```


# manifest example
emoji   short = hand  src = blah/blah/hand.svg   color = v1 v2 v3

# out folder
out

# directory format example
/something/%c/%s

# output (assuming it's a PNG)
out/something/v1/hand.png # the resulting image would contain v1's colormap
out/something/v2/hand.png # the resulting image would contain v2's colormap
out/something/v3/hand.png # the resulting image would contain v3's colormap

```

You should only use this for folders. If you want to use colourmap in your emoji's filename, use the formatting for shortcodes and values in the manifest instead.

---


## File structure to the source image (`%d`)

It's a little hard to verbally explain, but this inserts the folder structure leading to your source image for this emoji.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg

# out folder
whatever

# directory format example
%d/%s

# output (assuming it's a PNG)
whatever/blah/blah/hand.png

```

As you can see in this example, every folder leading up to the source SVG ('blah/blah/') is inserted into the directory path to the output wherever you put `%d`.

This is really useful if you want to folder your image output into relevant categories or groups.

----

## Export format (`%f`)

Inserts the [image format name](image_formats.md). (ie. `png-32`, `svg`, `jxl-128`, etc.)

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg

# out folder
final

# directory format example
final/something/%f/%s

# output (assuming it's a PNG at 32px)
final/something/png-32/hand.png

```
----
## Export format by itself (`%i`)

Inserts the [image format name](image_formats.md) without size. (ie. `png`, `svg`, `jxl`, etc.)

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg

# out folder
final

# directory format example
final/something/%i/%s

# output (assuming it's a PNG)
final/something/png/hand.png

```
---

## Export size (`%z`)

Inserts the [size declared in the image format](image_formats.md) (ie. `32`, `128`, `512`, etc.)
If it's an SVG (which has no size), it will return '0'.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg

# out folder
final

# directory format example
final/%i/%z/%s

# output (assuming it's a PNG at 128px)
final/png/128/hand.png

```
---
## Shortcode (`%s`)

Inserts the emoji's shortcode.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg

# out folder
hey

# directory format example
%f/%d/%s

# output (assuming it's a PNG at 32px)
hey/png-32/blah/blah/hand.png

```

----

## Codepoint (`%u`)

Inserts the emoji's unicode codepoint sequence.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg  code = #270b

# out folder
codepoint

# directory format example
%f/%u

# output (assuming it's a PNG at 32px)
codepoint/png-32/270b.png

```

----

## Bundle (`%b`)

Inserts the bundle the emoji belongs to.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg  bundle = core   code = #270b

# out folder
codepoint

# directory format example
%b-%f/%u

# output (assuming it's a PNG at 32px)
core-codepoint/png-32/270b.png

```

----

## Custom property **%(property_name)**

Inserts a the value for a specific property. Useful for properties that the default arguments don't cover or for leveraging your own custom properties.

```
# manifest example
emoji   short = hand  src = blah/blah/hand.svg   cat = expressions

# out folder
my-emoji

# directory format example
%(cat)/%s

# output (assuming it's a PNG at 32px)
my-emoji/expressions/hand.png

```
