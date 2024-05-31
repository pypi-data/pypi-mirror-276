<!--
SPDX-FileCopyrightText: 2024 Ledger SAS

SPDX-License-Identifier: Apache-2.0
-->

# dts-utils python package
`dts-utils` is an utility python package that aims to ease dts handling in python and source code
generation based on dts files. Dts file parsing, preprocessing, validation are **out of scope** of
this package. This package is built on top of [Zephyr](https://github.com/zephyrproject-rtos/zephyr)
[devicetree](https://pypi.org/project/devicetree/) package.

This package was built to fit OutpostOS needs but was designed to be generic enough and code
generation language agnostic. Thus, this package can be used by any project which need to use
dts files and generate code source or anything else based on it.

Provided [dts2src entrypoint](#dts2src-entrypoint) is based on Jinja2 template processing, allowing
users to fully controlled generated output by providing his/her very own templates.

## Dependencies
 - Python >= 3.10
 - Jinja2 >= 3
 - devicetree >= 0.0.2
 - rich

## Prerequisites
One may read, as an introduction, the following documentation:
 - [Jinja2 template writing](https://jinja.palletsprojects.com/en/3.1.x/templates/)
 - [Devicetree specification](https://www.devicetree.org/)
 - [Zephyr devicetree.dtlib](https://python-devicetree.readthedocs.io/en/latest/dtlib.html)

## Usage
`dts_utils.Dts` is the based class, it uses internally `devicetree.dtlib.Dts` and ease handling
by extending class attributes with `__getattr__`. For `Dts` object, attributes are resolved, in
order, from aliases and then in root `Node`. For `Node`, attribute are resolved from child node,
label and, then, property. `Property` are  converted according to internal dtlib value type.

Accessing a property or child node is straightforward and simply need to use the dot (`.`)
notation. If node or property contain special characters (e.g. `@`, `,`, `#`, `-`) in their name, one
should use [`getattr`](https://docs.python.org/3/library/functions.html#getattr) python built-in.

```python
import dts_utils

dts = dts_utils.Dts('/path/to/dts/file')

# get root node
root = dts.root

# get soc node
soc = dts.soc

# get usart1 device node by label
# labeled node are accessible from dts file or parent node
usart1 = dts.usart1
# OR
usart1 = soc.usart1

# get usart1 device node by name
usart1 = getattr(dts, 'usart@4xxxxxxx')
```

### dts_dump entrypoint

Command line entrypoint that can dump in a pretty formatted form the dts file.

```console
$ dts_dump --help
usage: dts_dump [-h] [-s] [-v] dts [node]

dump a dts in a human readable format

positional arguments:
  dts                dts file
  node               filter on node name or label

options:
  -h, --help         show this help message and exit
  -s, --status-okay  dump only status=okay nodes, except clocks
  -v, --version      show program's version number and exit
```
Example:
```console
$ dts_dump /path/to/dts usart1
usart1: serial@40013800 {
        compatible = "st,stm32-usart", "st,stm32-uart";
        reg = < 0x40013800 0x400 >;
        clocks = < &rcc 0xa4 0x4000 >;
        resets = < &rctl 0xf8e >;
        interrupts = < 0x3d 0x0 >;
        status = "okay";
        pinctrl-0 = < &usart1_tx_pc1 >, < &usart1_rx_pc0 >;
        phandle = < 0x7 >;
};
```

### dts2src entrypoint
`dts2src` entrypoint is a helper command line tool that process Jinja2 templates with the given
dts file. To ease template writing, built-in jinja extension `loopcontrol` is enabled, dts object
and environment variables are pass to the jinja environment along with custom jinja filters and
tests

```console
$ dts2src --help
usage: dts2src [-h] -d DTS -t TEMPLATE [-v] output

render jinja2 template using dts as data source

positional arguments:
  output                output filename

options:
  -h, --help            show this help message and exit
  -d DTS, --dts DTS     dts file to use as data source
  -t TEMPLATE, --template TEMPLATE
                        source template in jinja2 syntax
  -v, --version         show program's version number and exit
```


#### access to dts node and property
From Jinja environment, `dts_utils.Dts` is available as `dts`.
Each nodes and/or properties are available using the dot (`.`) operator or `[]` operator (this is
required if node or porperty name contains special characters).

e.g.
```jinja
{{ dts.soc }}
```
or
```jinja
{{ dts.usart1['pinctrl-0'] }}
```

#### access to environment variable
Environment variables are available, without external jinja extensions. Those are available as a
dictionary named `env`.

e.g.
```jinja
{{ env.USER }}
```

<!--
   Add custom filters/tests ref
   do not duplicate documentation entries
   Those are documented with pythondoc and generated with sphinx
-->

<!-- TODO
## Contributing
-->

## License
```
Copyright 2023 - 2024 Ledger SAS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
