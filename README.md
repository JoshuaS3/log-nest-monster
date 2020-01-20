<p align="center" id="lnm">
  <img src="/static/logobanner.png"/>
</p>
<p align="center">
  <i><b>(WIP)</b> A lightweight C logging library and parser for event-oriented logs.</i>
</p>
<p align="center">
  <img src="https://img.shields.io/github/license/joshuas3/lognestmonster?style=flat-square"/>
  <img src="https://img.shields.io/badge/version-0.3.0-informational?style=flat-square"/>
  <img src="https://img.shields.io/github/size/joshuas3/lognestmonster/src/c/lognestmonster.h?label=header%20size&style=flat-square"/>
  <img src="https://img.shields.io/codacy/grade/15048b0c7728497394651e295d61746b/dev?logo=codacy&style=flat-square"/>
  <a href="https://travis-ci.com/JoshuaS3/lognestmonster">
    <img src="https://img.shields.io/travis/joshuas3/lognestmonster/dev?logo=travis&style=flat-square"/>
  </a>
  <a href="https://github.com/JoshuaS3/lognestmonster/actions">
    <img src="https://img.shields.io/github/workflow/status/JoshuaS3/lognestmonster/C Header Unit Tests?label=C%20Header%20Unit%20Tests&logo=github&style=flat-square"/>
  </a>
<p>

Lognestmonster is a general-purpose single-header C logging library that pertains a number of features:
 - Nested/layer-based logging capabilities
 - Event-oriented log compilation
 - Multiple queues or outputs
 - Full developer customizability on memory allocation
   * Preprocessor handles to incorporate non-standard memory functions
 - Full developer customizability on I/O redirection
   * Generic filesystem log output
   * End-to-end `stdout` and `stdin` piping, allowing data transfer over serial, socket, or anything else
 - A binary format lighter than plaintext
 - A feature-packed but comprehensive standalone deserializer/parser
   * Interactive textual UI (ncurses)
   * Logtree filtering/sorting and navigation
   * Data operations such as binary to plaintext conversions and custom hooks on user-defined events
   * Optional daemon for hook events
   * Full developer customizability on data display, program controls, and hook operations

<i><b>(WIP)</b> Not yet meant for development or production use</i>

## Copyright

This package is copyrighted by [Joshua 'joshuas3' Stockin](https://joshstock.in/) and licensed under the [MIT License](LICENSE).

A form of the following should be present in each major library source or header file.
```
lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin
<https://joshstock.in>
<https://github.com/JoshuaS3/lognestmonster>
This software is licensed under the MIT License.
```
