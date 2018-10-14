orxporter
=========

Emoji exporter used for Mutant Standard emoji set

Introduction
------------

Orxporter was created as a rewrite of scripts used to automate some of the
workflow for Mutant Standard. Its purpose remains to be the primary build tool
for Mutant Standard packages, and so its features remain largely constrained
to a single use case.

That said, there has been interest in this tool, as it allows custom builds
or modifications of Mutant Standard packages, and is generic enough to work
for similar projects.

Disclaimer
----------

Orxporter is an open-sourced insider tool, and was never meant to be used at
large. There has been no significant effort to design, test, or follow any
good practice. Bugs at edge cases are known about and ignored. As long as
Mutant Standard is built properly according to Dzuk's wishes, it's unlikely
any features will be added or bugs fixed.

Features
--------

* Declarative language for defining semantics of emoji set
* Color mapping (recoloring)
* Unicode metadata
* SVG and arbitrary size PNG exports
* JSON output of emoji set metadata
* Output options including emoji filtering, customisable export directory
  structure and filenaming
* Embedding licensing metadata
* Multithreading

Prerequisites
-------------

* Python 3
* ImageMagick or any other tool capable of converting SVG to PNG (only for
  raster outputs)

Installation
------------

None required.
