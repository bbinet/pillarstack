# PillarStack

This custom saltstack `ext_pillar` is inspired by
[varstack](https://github.com/conversis/varstack) but is heavily based on
Jinja2 for maximum flexibility.

It supports the following features:
  - multiple config files that are jinja2 templates with support for `pillar`,
    `__grains__`, `__salt__`, `__opts__` objects
  - a config file renders as an ordered list of files (paths of these files are
    relative to the current config file)
  - this list of files are read in ordered as jinja2 templates with support for
    `stack`, `pillar`, `__grains__`, `__salt__`, `__opts__` objects
  - all these rendered files are then parsed as `yaml`
  - then all yaml dicts are merged in order with support for the following
    merging strategies: `merge-first`, `merge-last`, and `overwrite`
  - stack config files can be matched based on `pillar`, `grains`, or `opts`
    values, which make it possible to support kind of self-contained
    environments

## Installation

Installing the PillarStack `ext_pillar` is as simple as dropping the stack.py
file in the `<extensions_modules>/pillar` directory (no external python module
required).

## Configuration in Salt

Like any other external pillar, its configuration takes place through the
`ext_pillar` key in the master config file.

However, you can configure PillarStack in 3 different ways:

### Single config file

This is the simplest option, you just need to set the path to your single
PillarStack config file like below:

    ext_pillar:
      - stack: /path/to/stack.cfg

### List of config files

You can also provide a list of config files:

    ext_pillar:
      - stack:
          - /path/to/stack1.cfg
          - /path/to/stack2.cfg

### Select config files through grains|pillar|opts matching

You can also opt for a much more flexible configuration: PillarStack allows to
select the config files for the current minion based on matching values from
either grains, or pillar, or opts objects.

Here is an example of such a configuration, which should speak by itself:

    ext_pillar:
      - stack:
          pillar:environment:
            dev: /path/to/dev/stack.cfg
            prod: /path/to/prod/stack.cfg
          grains:custom:grain:
            value:
              - /path/to/stack1.cfg
              - /path/to/stack2.cfg
          opts:custom:opt:
            value: /path/to/stack0.cfg
