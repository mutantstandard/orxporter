# Metadata (Licenses)

Orxporter can embed metadata into your resulting emoji. This is useful if you want to put author or license information into your work for public distribution.

You add metadata to your manifests using the orx keyword `license`, as shown below:

```
license svg = license/svg.xml		exif = license/exif.json
```

Metadata is automatically embedded in your resulting images, but if you want to leave it out...

- Use the flag `-l` if you're using the [simple exporting method](image_easy,md).
- Use `license = no` in your Parameters file if you're using the [advanced exporting method](image_advanced),

Metadata embedding is only done with certain formats:

- EXIF metadata can be embedded in PNG and AVIF files.
- SVG metadata can be embedded in SVG files.

---

## `svg`: SVG Metadata

SVG Metadata is an XML file you create that contains stuff that gets inserted in the `<metadata>` tag of your resulting SVGs.

Below is an example XML file with Mutant Standard's SVG metadata:

```
<rdf:RDF xmlns:cc="http://web.resource.org/cc/"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:dc = "http://purl.org/dc/elements/1.1/"
         >

     <rdf:Description rdf:about="">
       <dc:title>Mutant Standard emoji v0.4.1</dc:title>
     </rdf:Description>

    <cc:work rdf:about="">
        <cc:license rdf:resource="http://creativecommons.org/licenses/by-nc-sa/4.0/"/>
        <cc:attributionName>Dzuk</cc:attributionName>
        <cc:attributionURL>http://mutant.tech/</cc:attributionURL>
    </cc:work>

</rdf:RDF>
```

---

## `exif`: EXIF Metadata

EXIF Metadata is a JSON file you create that contains stuff that gets inserted in the EXIF metadata of your resulting raster images.

Below is an example JSON file with Mutant Standard's EXIF metadata:

```
{
    "XMP-dc:title": "Mutant Standard emoji v0.4.1",
    "XMP-dc:rights": "This work is licensed to the public under the Attribution-NonCommercial-ShareAlike 4.0 International license https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "XMP-xmpRights:UsageTerms": "This work is licensed to the public under the Attribution-NonCommercial-ShareAlike 4.0 International license https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "XMP-cc:AttributionName": "Dzuk",
    "XMP-cc:AttributionURL": "mutant.tech",
    "XMP-cc:License": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
}

```
