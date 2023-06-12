Manifests
=========

Introduction
------------

Orxporter manifest defines semantics of an emoji set. This does not include
output settings, in order to allow the same manifest to be reused to create
packages in different formats or with different directory structures.

Because a set can contain thousands of emoji, Orxporter uses a custom lightweight data serialisation format to contain your emoji metadata.


Syntax
------

An expression contains an **instruction keyword**, like 'emoji', 'colormap', etc., followed by parameters. Parameters are typically key-value pairs, but some instructions require a name argument which must be passed first. To explicitly pass an empty value, use **!**.

```
colormap default
    src     = key
    dst     = y1
    short    = !
    code = !
```

Each statement starts at the beginning of a line. Whitespace (spaces, tabs etc)
at the beginning of a line imply continuation of a statement. These two
statements are identical:

```
emoji short=dark_elf src=dark_elf.svg code=!undefined cat=people
```

```
emoji
    short    = dark_elf
    src     = dark_elf.svg
    code = !undefined
    cat     = people
```

Comments
--------

Commented lines start with __#__:

```
# This is a comment
```

Variables
---------

The dollar sign (__$__) is used for variable names. So **$cmaps_all** inserts the
value of the previously defined variable **cmaps_all**. In order to
disambiguate syntax, it is possible to wrap the variable name in parentheses.

Please note that "variable" is a misnomer because they're actually constant. In
fact, if you try to redefine a variable, Orxporter will rightfully protest.

This is how a variable is defined:

```
define cmap_set_hmn h1 h2 h3 h4 h5
```

Now, every occurence of **$cmap_set_hmn** will be replaced by **h1 h2 h3 h4 h5**.
It is also possible to use previously defined variables in a _define_
statement:

```
define cmaps_all $cmap_def $cmap_set_shared $cmap_set_hmn $cmap_set_fur
```

Emoji definitions
-----------------

Emoji are defined using _emoji_ instruction. The most important parameters are:

* _src_     -- source image file
* _short_    -- shortcode (optional)
* _code_ -- unicode codepoint sequence (optional)
* _color_   -- list of color mappings to use (optional)

Let's look at an example:

```
emoji
    short    = facepalm%c
    src     = $(semi_body_path)/facepalm.svg
    color   = $cmaps_all
    code = #1F926 %u
```

We are using **cmaps_all** (which we have already defined) as the list of color
mappings for this emoji design, but we could also be explicit:

```
    color   = h1 h2 h3 h4 h5 b1 b2 b3 g1 [and so on...]
```

Orxporter will generate a separate emoji for each colormap. It is important
(and mandatory) to ensure that the shortcodes and unicode sequences are unique.
In our example we can see the formatting codes **%c** and **%u** used to insert the
colormap's shortcode and unicode sequence respectively.

Colormaps and palettes
----------------------

Orxporter uses colormaps and palettes to allow the same design to be
reused in different color schemes as separate emoji.

A palette is a list of named colors, and is defined like so:

```
palette v1
    skin_shade_1    = #827599
    skin_shade_2    = #664E79
    skin_shade_3    = #2E1D46
    nail_care_color = #17DA55
    paw_pad_color   = #4D3A6E

    shirt_shade_1   = $shirt_shade_1
    shirt_shade_2   = $shirt_shade_2
    shirt_shade_3   = $shirt_shade_3
```

A colormap is a translation from one palette to another. It may have its own
shortcode and unicode sequence, which can be referred to in an emoji definition
via **%c** and **%u** formatting codes respectively. Its definition takes the
following arguments:

* _src_     -- source palette
* _dst_     -- target palette
* _short_    -- shortcode
* _code_ -- unicode sequence; use **!undefined** to explicitly omit assigning
a value, otherwise Orxporter will assume it was unintentional and throw an error
whenever a value is expected

```
colormap v1
    src     = key
    dst     = v1
    short    = _v1
    code = !undefined
```

When recoloring, Orxporter will detect the presence of colors from the source
palette, and replace them with corresponding colors from the target palette.

Note that Mutant Standard currently uses **key** palette for its source
images, thus that is the source for all its colormaps.

Includes
--------

It is possible to import other manifest files, allowing modularity and reuse:

```
include colors/c_const.orx
```

Imported manifests may also use the *include* instruction, but note that the
pathnames are always relative to the original manifest.

Formatting codes
----------------

The following formatting codes are supported:

* **$var**, **$(var)** - insert the value of variable **var**
* **%c** - insert the shortcode associated with current emoji's colormap
* **%C** - same as **%c**, but prepend with underscore (**_**) if not empty
* **%u** - insert the unicode sequence associated with current emoji's colormap
* **%U** - same as %u, except if non-empty precede with ZWJ code
* **%(param)** - insert the value of emoji's parameter **param**

Unicode
-------

Unicode sequence values are written as space-separated codepoint values.
Numbers prefixed with a hash sign **#** are parsed as hexadecimal:

```
emoji [...] code = #100666 #101337
```

To specify an empty (zero-length) sequence, pass an empty value (**!**):

```
colormap [...] code = !
```

To explicitly undefine a unicode sequence value for an emoji, pass
**!undefined**. This will tell Orxporter to omit this emoji (instead of
throwing an error) when exporting unicode-named files:

```
emoji [...] code = !undefined
```

Classes
-------

A class is a set of emoji parameter values. Its purpose is to group emoji
allowing their common parameter values to be changed in one place. A class is
defined as such:

```
class paw
    morph = paw
    color = $cmaps_fur
```

Emoji may belong to one or more classes and thus inherit their parameter
values. Note that in case of conflict, the values of classes listed later
override those of classes listed earlier, which in turn get overridden by the
explicit parameters of the *emoji* keyword:

```
emoji human_paw
    class = paw
    color = $cmaps_hmn
```

Finally, classes can inherit from other classes by passing their names before
the list of key-value parameters:

```
class cat_paw paw cats
    color = $cmaps_cat
```

Custom parameters
-----------------

It is possible to use custom key-value parameters. They can then be refered to
using formatting codes, or exported along with any other metadata using the
**-j** switch.

Some of the undocumented parameters are used for the **-J** export switch for
purposes of the Mutant Standard website.

Licensing
---------

Orxporter will embed licensing metadata to each exported SVG and PNG file if
defined using the *license* keyword:

```
license
    svg = svg_license
    exif = exif.json
```

The *svg* parameter must point to a file containing the desired string to be
inserted inside each SVG file's *metadata* tag.

The *exif* parameter must point to a JSON file containing a single object with
the desired EXIF tags to be written to each PNG file.

Text descriptions
-----------------

Emoji and colormaps may define text descriptions using the **desc** property.
Recolored emoji will have their text description appended with the description
of the colormap.

This feature is probably only useful in conjunction with the **-j** switch.
