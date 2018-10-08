Introduction
============

Orxporter *manifest* defines semantics of an emoji set. This does not include
output settings, in order to allow the same *manifest* to be reused to create
packages in different formats or with different directory structures.

The *manifests* use a simple custom declarative language, which due to demand
was designed to be light and readable. However, it was also designed to get
the job done and nothing else. No significant effort has or will be made to
formalise the language, to ensure it always parses correctly, or to catch
errors.

Quick start
===========

This is a quick introduction to the most important features of the language.
The subsequent sections provide a more complete reference.

Syntax
------

An expression contains an instruction name, followed by parameters. Parameters
are typically key-value pairs, but some instructions require a name argument
which must be passed first. To explicitly pass an empty value, use **!**.

```
colormap default
    src     = key
    dst     = y1
    code    = !
    unicode = !
```

Each statement starts at the beginning of a line. Whitespace (spaces, tabs etc)
at the beginning of a line imply continuation of a statement. These two
statements are identical:

```
emoji code=dark_elf src=dark_elf.svg unicode=!undefined cat=people
```

```
emoji
    code    = dark_elf
    src     = dark_elf.svg
    unicode = !undefined
    cat     = people
```

Comments
--------

Commented lines start with _#_:

```
# This is a comment
```

Variables
---------

The dollar sign (_$_) is used for variable names. Thus *$cmaps_all* inserts the
value of the previously defined variable **cmaps_all**. In order to
disambiguate syntax, it is possible to wrap the variable name in parentheses.

Please note that "variable" is a misnomer because they're actually constant. In
fact, if you try to redefine a variable, orxporter will rightfully protest.

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
* _code_    -- shortcode (optional)
* _unicode_ -- unicode sequence (optional)
* _color_   -- list of color mappings to use (optional)

Let's look at an example:

```
emoji
    code    = facepalm%c
    src     = $(semi_body_path)/facepalm.svg
    color   = $cmaps_all
    unicode = #1F926 %u
```

We are using **cmaps_all** (which we have already defined) as the list of color
mappings for this emoji design, but we could also be explicit:

```
    color   = h1 h2 h3 h4 h5 b1 b2 b3 g1 [and so on...]
```

Orxporter will generate a separate emoji for each colormap. It is important
(and mandatory) to ensure that the shortcodes and unicode sequences are unique.
In our example we can see the formatting codes *%c* and *%u* used to insert the
colormap's shortcode and unicode sequence respectively.

Colormaps and palettes
----------------------

Orxporter uses *colormaps* and *palettes* to allow the same design to be
reused in different color schemes as separate emoji.

A *palette* is a list of named colors, and is defined like so:

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

A *colormap* is a translation from one *palette* to another. It may have its own
shortcode and unicode sequence, which can be refered to in an emoji definition
via *%c* and *%u* formatting codes respectively. Its definition takes the
following arguments:

* _src_     -- source *palette*
* _dst_     -- target *palette*
* _code_    -- shortcode
* _unicode_ -- unicode sequence; use **!undefined** to explicitly omit assigning
a value, otherwise orxporter will assume it was unintentional and throw an error
whenever a value is expected

```
colormap v1
    src     = key
    dst     = v1
    code    = _v1
    unicode = !undefined
```

When recoloring, orxporter will detect the presence of colors from the source
*palette*, and replace them with corresponding colors from the target *palette*.

Note that Mutant Standard currently uses **key** *palette* for its source
images, thus that is the source for all its *colormaps*.

Includes
--------

It is possible to import other *manifest* files, allowing modularity and reuse:

```
include colors/c_const.orx
```

Imported *manifests* can also use the *include* instruction, but note that the
pathnames are always relative to the original *manifest*.
