import argparse
from textwrap import dedent

import mdformat

from mdformat_lists._plugin import ListsPlugin


def _format_with_bullet(text, bullet=None, ordered_marker=None, number=False):
    plugin_opts = {}
    if bullet is not None:
        plugin_opts["bullet"] = bullet
    if ordered_marker is not None:
        plugin_opts["ordered_marker"] = ordered_marker
    options = {}
    if plugin_opts:
        options["plugin"] = {"lists": plugin_opts}
    if number:
        options["number"] = True
    return mdformat.text(text, extensions=["lists"], options=options)


class TestDefaultBullet:
    def test_simple_list(self):
        input_md = dedent("""\
            * item 1
            * item 2
        """)
        result = _format_with_bullet(input_md)
        assert result == dedent("""\
            - item 1
            - item 2
        """)

    def test_preserves_content(self):
        input_md = dedent("""\
            * hello world
        """)
        result = _format_with_bullet(input_md)
        assert result == dedent("""\
            - hello world
        """)

    def test_consecutive_lists_alternate(self):
        input_md = dedent("""\
            - a

            * b
        """)
        result = _format_with_bullet(input_md)
        assert result == dedent("""\
            - a

            * b
        """)


class TestDashBullet:
    def test_simple_list(self):
        input_md = dedent("""\
            * item 1
            * item 2
        """)
        result = _format_with_bullet(input_md, bullet="-")
        assert result == dedent("""\
            - item 1
            - item 2
        """)

    def test_converts_from_plus(self):
        input_md = dedent("""\
            + item 1
            + item 2
        """)
        result = _format_with_bullet(input_md, bullet="-")
        assert result == dedent("""\
            - item 1
            - item 2
        """)

    def test_consecutive_lists_alternate(self):
        input_md = dedent("""\
            - a

            * b
        """)
        result = _format_with_bullet(input_md, bullet="-")
        assert result == dedent("""\
            - a

            * b
        """)


class TestAsteriskBullet:
    def test_simple_list(self):
        input_md = dedent("""\
            - item 1
            - item 2
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * item 1
            * item 2
        """)

    def test_converts_from_plus(self):
        input_md = dedent("""\
            + item 1
            + item 2
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * item 1
            * item 2
        """)


class TestPlusBullet:
    def test_simple_list(self):
        input_md = dedent("""\
            - item 1
            - item 2
        """)
        result = _format_with_bullet(input_md, bullet="+")
        assert result == dedent("""\
            + item 1
            + item 2
        """)

    def test_converts_from_asterisk(self):
        input_md = dedent("""\
            * item 1
            * item 2
        """)
        result = _format_with_bullet(input_md, bullet="+")
        assert result == dedent("""\
            + item 1
            + item 2
        """)


class TestNestedLists:
    def test_nested_list(self):
        input_md = dedent("""\
            - item 1
              - nested 1
              - nested 2
            - item 2
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * item 1
              * nested 1
              * nested 2
            * item 2
        """)

    def test_deeply_nested(self):
        input_md = dedent("""\
            - a
              - b
                - c
        """)
        result = _format_with_bullet(input_md, bullet="+")
        assert result == dedent("""\
            + a
              + b
                + c
        """)


class TestConsecutiveLists:
    """Consecutive bullet lists alternate markers to stay as separate lists.

    The plugin should alternate between the configured bullet and `-`.
    """

    def test_asterisk_alternates_with_dash(self):
        input_md = dedent("""\
            * a

            - b
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * a

            - b
        """)

    def test_plus_alternates_with_dash(self):
        input_md = dedent("""\
            + a

            - b
        """)
        result = _format_with_bullet(input_md, bullet="+")
        assert result == dedent("""\
            + a

            - b
        """)

    def test_three_consecutive_lists(self):
        input_md = dedent("""\
            * a

            - b

            * c
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * a

            - b

            * c
        """)


class TestTightAndLooseLists:
    def test_tight_list(self):
        input_md = dedent("""\
            - item 1
            - item 2
            - item 3
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * item 1
            * item 2
            * item 3
        """)

    def test_loose_list(self):
        input_md = dedent("""\
            - item 1

            - item 2

            - item 3
        """)
        result = _format_with_bullet(input_md, bullet="*")
        assert result == dedent("""\
            * item 1

            * item 2

            * item 3
        """)


class TestDefaultOrderedMarker:
    def test_simple_list(self):
        input_md = dedent("""\
            1) item 1
            2) item 2
        """)
        result = _format_with_bullet(input_md)
        assert result == dedent("""\
            1. item 1
            1. item 2
        """)

    def test_preserves_content(self):
        input_md = dedent("""\
            1) hello world
        """)
        result = _format_with_bullet(input_md)
        assert result == dedent("""\
            1. hello world
        """)


class TestDotOrderedMarker:
    def test_simple_list(self):
        input_md = dedent("""\
            1) item 1
            2) item 2
        """)
        result = _format_with_bullet(input_md, ordered_marker=".")
        assert result == dedent("""\
            1. item 1
            1. item 2
        """)

    def test_converts_from_paren(self):
        input_md = dedent("""\
            1) item 1
            2) item 2
        """)
        result = _format_with_bullet(input_md, ordered_marker=".")
        assert result == dedent("""\
            1. item 1
            1. item 2
        """)


class TestParenOrderedMarker:
    def test_simple_list(self):
        input_md = dedent("""\
            1. item 1
            2. item 2
        """)
        result = _format_with_bullet(input_md, ordered_marker=")")
        assert result == dedent("""\
            1) item 1
            1) item 2
        """)

    def test_converts_from_dot(self):
        input_md = dedent("""\
            1. item 1
            2. item 2
        """)
        result = _format_with_bullet(input_md, ordered_marker=")")
        assert result == dedent("""\
            1) item 1
            1) item 2
        """)


class TestConsecutiveOrderedLists:
    def test_ordered_lists_separated_by_content_keep_primary_marker(self):
        """Ordered lists separated by other content are not consecutive siblings,
        so they all use the primary marker."""
        input_md = dedent("""\
            1. a

            Some text.

            1. b
        """)
        result = _format_with_bullet(input_md, ordered_marker=".")
        assert result == dedent("""\
            1. a

            Some text.

            1. b
        """)

    def test_ordered_lists_separated_by_content_paren_marker(self):
        input_md = dedent("""\
            1. a

            Some text.

            1. b
        """)
        result = _format_with_bullet(input_md, ordered_marker=")")
        assert result == dedent("""\
            1) a

            Some text.

            1) b
        """)


class TestConsecutiveNumbering:
    def test_consecutive_numbering(self):
        input_md = dedent("""\
            1. item 1
            2. item 2
            3. item 3
        """)
        result = _format_with_bullet(input_md, number=True)
        assert result == dedent("""\
            1. item 1
            2. item 2
            3. item 3
        """)

    def test_consecutive_numbering_with_paren_marker(self):
        input_md = dedent("""\
            1. item 1
            2. item 2
            3. item 3
        """)
        result = _format_with_bullet(input_md, ordered_marker=")", number=True)
        assert result == dedent("""\
            1) item 1
            2) item 2
            3) item 3
        """)


class TestAddCliArgumentGroup:
    def test_adds_bullet_and_ordered_marker_arguments(self):
        parser = argparse.ArgumentParser()
        group = parser.add_argument_group("lists")
        ListsPlugin.add_cli_argument_group(group)
        args = parser.parse_args([])
        assert args.bullet == "-"
        assert args.ordered_marker == "."

    def test_bullet_argument_accepts_valid_choices(self):
        parser = argparse.ArgumentParser()
        group = parser.add_argument_group("lists")
        ListsPlugin.add_cli_argument_group(group)
        args = parser.parse_args(["--bullet", "*"])
        assert args.bullet == "*"

    def test_ordered_marker_argument_accepts_valid_choices(self):
        parser = argparse.ArgumentParser()
        group = parser.add_argument_group("lists")
        ListsPlugin.add_cli_argument_group(group)
        args = parser.parse_args(["--ordered-marker", ")"])
        assert args.ordered_marker == ")"


class TestNestedOrderedLists:
    def test_nested_ordered_list(self):
        input_md = dedent("""\
            1. item 1
               1. nested 1
               2. nested 2
            2. item 2
        """)
        result = _format_with_bullet(input_md, ordered_marker=")")
        assert result == dedent("""\
            1) item 1
               1) nested 1
               1) nested 2
            1) item 2
        """)


class TestTightAndLooseOrderedLists:
    def test_tight_ordered_list(self):
        input_md = dedent("""\
            1. item 1
            2. item 2
            3. item 3
        """)
        result = _format_with_bullet(input_md, ordered_marker=")")
        assert result == dedent("""\
            1) item 1
            1) item 2
            1) item 3
        """)

    def test_loose_ordered_list(self):
        input_md = dedent("""\
            1. item 1

            2. item 2

            3. item 3
        """)
        result = _format_with_bullet(input_md, ordered_marker=")")
        assert result == dedent("""\
            1) item 1

            1) item 2

            1) item 3
        """)
