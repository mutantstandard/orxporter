# orx

Because emoji sets can involve hundreds or thousands of images, we needed a format to contain emoji data in a way that doesn't create too much whitespace and was really quick to type. Existing formats like JSON and YAML were not really made for this task, so Orxporter uses it's own format.


## Structure of an orx file

Every part of an orx file is a statement consisting of an **instruction keyword** followed by **parameters**.

You can write a statement in one line, or with the parameters indented - whitespaces (spaces, tabs, etc.) at the beginning of a line imply the continuation of a statement.

The following two statements are identical:


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



## Instruction keywords

Everything in orx consists of an expression beginning with a **instruction keyword** that declares what type of expression it is. You can't nest expressions.


```
# 'emoji' is the instruction keyword

emoji
    short = egg
    src = $(food_path)/other_fresh/egg.svg
    code = #1F95A
    cat = food_drink_herbs
    desc = egg
```

Some kinds of instruction keywords require a name argument first before parameters.

```
# 'palette' is the instruction keyword that requires a name argument (In this case, 'h2').

palette h2
    shade_1 = #885030
    shade_2 = #6C320E
    shade_3 = #3A1804

    nail_polish = #E9589E

    shirt_shade_1 = $shirt_shade_1
    shirt_shade_2 = $shirt_shade_2
    shirt_shade_3 = $shirt_shade_3

```


## Parameters

Depending on what kind of expression it is, the instruction keyword can have certain types of values attached to it.

There are two types of values - named values and unnamed values.

- **Named values** within an expression are simply noted with a '=' between the value name and the value itself.
- **Unnamed values** are simply typed after the expression name without any symbols or punctuation.

```
# no unnamed values, only named values
fish   param1 = meh    param2 = meh     

# JSON equivalent
{"fish": [], {"param1": "meh", "param2": "meh"}}
```

```
# multiple unnamed values but no named values
rabbit  meh more_meh even_more_meh

# JSON equivalent
{"rabbit": ["meh", "more_meh", "even_more_meh"], {}}
```

```
# both unnamed and named values
goose meh   param1 = meh    param 2 = meh

# JSON equivalent
{"rabbit": ["meh"], {"param1": "meh", "parah2": "meh"}}
```



You can also indent your named values like this...

```

fish
    param1 = meh
    param2 = meh     

goose meh   
    param1 = meh
    param2 = meh

```



## Values

Variable types are pretty implicit in Orxporter - unless it's a custom parameter, a particular type will be expected.

```

# string

string1 = weed
string2 = this is also perfectly valid, you don't need quotation marks


# hexadecimal number sequence
# (eg. for Unicode codepoint sequences)

hex = #101691
list_of_hex = #1f3f3 #200d #1f308

```






---

## Common instruction keywords

There are two consistent instruction keywords across any type of orx file:


## `define`

Define variables that can be referenced elsewhere.

```
define <name> <value>
```

You reference it later, in one of two ways:
- `$name` : for when you want to insert a variable into a parameter value or list
- `$(name)`: for when you want to insert a variable within a string.



You can use it to reference single values...

```
define vs16 #fe0f

define food_path food_drink_herbs

emoji
    short = plate
    src = $(food_path)/food/plate.svg
    code = #1F37D $vs16
    cat = food_drink_herbs
    desc = plate with a knife and fork
```

or use it to contain a list of values...


```
define cmap_set_hmn h1 h2 h3 h4 h5
```

or use it to add previously defined things together!

```
define cmaps_hmn $cmap_def $cmap_set_shared $cmap_set_hmn
```

The orx interpreter reads things sequentially; so you can't reference something before it's defined. If you want to use a variable later, you need to make sure the define declaration is done somewhere before...


## `include`

Using `include` attaches the contents of one orx file to the one with this statement.

Orxporter only accepts one manifest file, but you can split your files up and then attach them all together with this keyword. This lets you keep large emoji projects tidy.

```
include second_file.orx
# this pulls the contents of 'second_file.orx' and attaches it to this position.
```

`include` attaches the contents of the mentioned orx file to the position the `include` statement was made, so the whole manifest will be evaluated as if the file's contents exist at this position.

This is important because orx files are read sequentially - if you're referencing two manifests, emoji_pack_1.orx and emoji_pack_2.orx, but the first file has a variable the latter file needs, then you need to make sure the first one is included first and the second one is included afterwards.



## Comments

Comments are single-line only and are marked with a '#' at the beginning:

```
# ignored!!! Q_Q
```
