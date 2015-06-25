# pillarstack

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

Installing the pillarstack `ext_pillar` is as simple as dropping the stack.py
file in the `<extensions_modules>/pillar` directory (no external python module
required).
