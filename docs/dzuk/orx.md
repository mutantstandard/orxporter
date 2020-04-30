# orx

Because emoji sets can involve hundreds or thousands of images, we needed a format to contain emoji data in a way that doesn't create too much whitespace and was really quick to type. Existing formats like JSON and YAML were not really made for this task, so Orxporter uses it's own format.


## Structure of an orx file

orx files are very simple.

Everything in orx consists of an expression beginning with a **instruction keyword** that declares what type of expression it is. You can't nest expressions.


```
fish   param1 = meh    param2 = meh  
# 'fish' is the instruction keyword

```

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

Comments are single-line only and are marked with '#':

```
# ignored!!! Q_Q
```

---
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


## `include`

Attach the contents of one orx file to the one with this statement.

```
include second_file.orx
### this pulls the contents of 'second_file.orx' and attaches it to this position.
```


## `define`

Define data that can be referenced elsewhere.

```
define <name> <value>
```

You reference it later with a $ followed by it's name (`$name`), or like `$(name)`. The latter is good to know if you want to insert a variable within a string.



You can use it to add single values...

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

or reference things that have already been defined in a new way!

```
define cmaps_hmn $cmap_def $cmap_set_shared $cmap_set_hmn
```

The orx interpreter reads things sequentially; so you can't reference something before it's defined.
