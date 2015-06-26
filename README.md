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

## PillarStack configuration files

The config files that are referenced in the above `ext_pillar` configuration
are jinja2 templates which must render as a simple ordered list of `yaml` files
that will then be merged to build pillar data.

The path of these `yaml` files must be relative to the directory of the
PillarStack config file.

The following variables are available in jinja2 templating of PillarStack
configuration files:
  - `pillar`: the pillar data (as passed by Salt to our `ext_pillar` function)
  - `minion_id`: the minion id ;-)
  - `__opts__`: a dictionary of mostly Salt configuration options
  - `__grains__`: a dictionary of the grains of the minion making this pillar
    call
  - `__salt__`: a dictionary of Salt module functions, useful so you don't have
    to duplicate functions that already exist (note: runs on the master)
So you can use all the power of jinja2 to build you list

For example, you could have a PillarStack config file which looks like:

    $ cat /path/to/stack/config.cfg
    core.yml
    osarchs/{{ __grains__['osarch'] }}.yml
    oscodenames/{{ __grains__['oscodename'] }}.yml
    {%- for role in pillar.get('roles', []) %}
    roles/{{ role }}.yml
    {%- endfor %}
    minions/{{ minion_id }}.yml

And the whole directory structure could look like:

    $ tree /path/to/stack/
    /path/to/stack/
    ├── config.cfg
    ├── core.yml
    ├── osarchs/
    │   ├── amd64.yml
    │   └── armhf.yml
    ├── oscodenames/
    │   ├── wheezy.yml
    │   └── jessie.yml
    ├── roles/
    │   ├── web.yml
    │   └── db.yml
    └── minions/
        ├── test-1-dev.yml
        └── test-2-dev.yml

In the above PillarStack configuration, given that test-1-dev minion is an
amd64 platform running Debian Jessie, and which `roles` pillar is `["db"]`, the
following `yaml`files would be merged in order:
  - `core.yml`
  - `osarchs/amd64.yml`
  - `oscodenames/jessie.yml`
  - `roles/db.yml`
  - `minions/test-1-dev.yml`
