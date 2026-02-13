# mdformat-lists

[![Build Status](https://github.com/brendanmaguire/mdformat-lists/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/brendanmaguire/mdformat-lists/actions?query=workflow%3ACI+branch%3Amain+event%3Apush)
[![PyPI version](https://img.shields.io/pypi/v/mdformat-lists)](https://pypi.org/project/mdformat-lists)

A [mdformat](https://github.com/hukkin/mdformat) plugin to configure list markers for unordered and ordered lists.

By default, mdformat uses `-` as the bullet character (alternating with `*` for consecutive lists) and `.` as the ordered list marker. This plugin allows you to choose between `-`, `*`, and `+` for bullets, and `.` and `)` for ordered list markers.

## Usage

Install with:

```bash
pip install mdformat-lists
```

Then simply run mdformat as usual:

```bash
mdformat <filename>
```

### Configuration

#### Unordered list bullet

Configure the bullet character in `.mdformat.toml`:

```toml
[plugin.lists]
bullet = "*"
```

Or via the command line:

```bash
mdformat --bullet="*" <filename>
```

Valid values are `-` (default), `*`, and `+`.

#### Ordered list marker

Configure the ordered list marker in `.mdformat.toml`:

```toml
[plugin.lists]
ordered_marker = ")"
```

Or via the command line:

```bash
mdformat --ordered-marker=")" <filename>
```

Valid values are `.` (default) and `)`.

When multiple ordered lists appear consecutively, the plugin alternates between the primary and secondary marker (`.` and `)`) to prevent Markdown parsers from merging separate lists into one.
