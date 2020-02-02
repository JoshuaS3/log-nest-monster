<p align="center" id="lnm">
  <img src="/static/logobanner.png"/>
</p>
<p align="center">
  <i><b>(WIP)</b> A lightweight C logging library and parser for event-oriented logs.</i>
</p>
<p align="center">
  <a href="https://github.com/JoshuaS3/lognestmonster/blob/dev/LICENSE">
    <img src="https://img.shields.io/github/license/joshuas3/lognestmonster?style=flat-square"/>
  </a>
  <a href="https://github.com/JoshuaS3/lognestmonster/tree/dev">
    <img src="https://img.shields.io/badge/version-(WIP) 0.3.0-informational?style=flat-square"/>
  </a>
  <a href="https://github.com/JoshuaS3/lognestmonster/blob/dev/src/c/lognestmonster.h">
    <img src="https://img.shields.io/github/size/joshuas3/lognestmonster/src/c/lognestmonster.h?label=header%20size&style=flat-square"/>
  </a>
  <a href="https://app.codacy.com/manual/JoshuaS3/lognestmonster/dashboard">
    <img src="https://img.shields.io/codacy/grade/15048b0c7728497394651e295d61746b/dev?logo=codacy&style=flat-square"/>
  </a>
  <a href="https://travis-ci.com/JoshuaS3/lognestmonster">
    <img src="https://img.shields.io/travis/joshuas3/lognestmonster/dev?logo=travis&style=flat-square"/>
  </a>
  <a href="https://github.com/JoshuaS3/lognestmonster/actions">
    <img src="https://img.shields.io/github/workflow/status/JoshuaS3/lognestmonster/C Header Unit Tests?label=C%20Header%20Unit%20Tests&logo=github&style=flat-square"/>
  </a>
<p>

Lognestmonster is a general-purpose single-header C logging library that
pertains a number of features:

* Nested/layer-based logging capabilities
* Event-oriented log compilation
* Multiple queues or outputs
* Full developer customizability on memory allocation
  * Preprocessor handles to incorporate non-standard memory functions
* Full developer customizability on I/O redirection
  * Generic filesystem log output
  * End-to-end `stdout` and `stdin` piping, allowing data transfer over serial,
    socket, or anything else
* A binary format lighter than plaintext
* A feature-packed but comprehensive standalone deserializer/parser
  * Interactive textual UI (ncurses)
  * Logtree filtering/sorting and navigation
  * Data operations such as binary to plaintext conversions and custom hooks on
    user-defined events
  * Optional daemon for hook events
  * Full developer customizability on data display, program controls, and hook
    operations

_**(WIP)** Not yet meant for development or production use_

## Performance at Different Optimization Levels

Output of `./test performance` as of commit `b54160c`:

Optimization Level | Header Binary Size\* (in bytes) | Unit Test Runtime\*\* (in µs)
------------------ | ------------------------------- | -----------------------------
-O0                | 22552                           | 70
-O1                | 18424                           | 67
-O2                | 22520                           | 69
-O3                | 26760                           | 68
-Os                | 18424                           | 69

\*Header binary size is measured by compilation of the following source file:

```c
// tests/header_only.c
#define LNM_INIT
#include "lognestmonster.h"

int main(void) {
    return 0;
}
```

\*\*Median taken from 200 trials run in sequence to account for variable processor
conditions and behaviors. Run on a mid-tier 3.3GHz processor (i5-4590). Runtime
is measured by the execution and output of [the header's unit
test](tests/header_unit.c).

## Copyright

This package is copyrighted by [Joshua 'joshuas3'
Stockin](https://joshstock.in/) and licensed under the [MIT License](LICENSE).

A form of the following should be present in each major library source or header
file.

```txt
lognestmonster Copyright (c) 2020 Joshua 'joshuas3' Stockin
<https://joshstock.in>
<https://github.com/JoshuaS3/lognestmonster>
This software is licensed under the MIT License.
```
