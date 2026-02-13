from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import argparse
    from collections.abc import Mapping

    from markdown_it import MarkdownIt

    from mdformat.renderer import RenderContext, RenderTreeNode
    from mdformat.renderer.typing import Render

DEFAULT_BULLET = "-"
VALID_BULLETS = ("-", "*", "+")

DEFAULT_ORDERED_MARKER = "."
VALID_ORDERED_MARKERS = (".", ")")


def _get_configured_bullet(context: RenderContext) -> str:
    plugin_opts = context.options.get("mdformat", {}).get("plugin", {}).get("lists", {})
    return plugin_opts.get("bullet", DEFAULT_BULLET)


def _get_configured_ordered_marker(context: RenderContext) -> str:
    plugin_opts = context.options.get("mdformat", {}).get("plugin", {}).get("lists", {})
    return plugin_opts.get("ordered_marker", DEFAULT_ORDERED_MARKER)


def _is_tight_list(node: RenderTreeNode) -> bool:
    # Copy of mdformat.renderer._util.is_tight_list
    assert node.type in {"bullet_list", "ordered_list"}

    # The list has list items at level +1 so paragraphs in those list
    # items must be at level +2 (grand children)
    for child in node.children:
        for grand_child in child.children:
            if grand_child.type != "paragraph":
                continue
            is_tight = grand_child.hidden
            if not is_tight:
                return False
    return True


def _get_list_marker_type(node: RenderTreeNode, primary_marker: str, secondary_marker: str) -> str:
    consecutive_lists_count = 1
    current = node
    while True:
        previous_sibling = current.previous_sibling
        if previous_sibling is None or previous_sibling.type != node.type:
            return primary_marker if consecutive_lists_count % 2 else secondary_marker
        consecutive_lists_count += 1
        current = previous_sibling


def _render_list(
    node: RenderTreeNode,
    context: RenderContext,
    markers: list[str],
) -> str:
    block_separator = "\n" if _is_tight_list(node) else "\n\n"
    indent_width = len(markers[0]) + 1

    with context.indented(indent_width):
        items = []
        for marker, child in zip(markers, node.children):
            item_text = child.render(context)
            lines = item_text.split("\n")
            first_line = lines[0]
            first = f"{marker} {first_line}" if first_line else marker
            rest = (f"{' ' * indent_width}{line}" if line else "" for line in lines[1:])
            items.append("\n".join([first, *rest]))
        return block_separator.join(items)


def _bullet_list(node: RenderTreeNode, context: RenderContext) -> str:
    primary_bullet = _get_configured_bullet(context)
    secondary_bullet = "*" if primary_bullet == "-" else "-"
    marker = _get_list_marker_type(node, primary_marker=primary_bullet, secondary_marker=secondary_bullet)
    return _render_list(node, context, [marker] * len(node.children))


def _ordered_list(node: RenderTreeNode, context: RenderContext) -> str:
    consecutive_numbering = context.options.get("mdformat", {}).get("number", False)
    primary_marker = _get_configured_ordered_marker(context)
    secondary_marker = ")" if primary_marker == "." else "."
    marker_type = _get_list_marker_type(node, primary_marker=primary_marker, secondary_marker=secondary_marker)

    starting_number = node.attrs.get("start")
    if starting_number is None:
        starting_number = 1
    assert isinstance(starting_number, int)

    list_len = len(node.children)

    if consecutive_numbering:
        pad = len(str(starting_number + list_len - 1))
        markers = [f"{str(starting_number + i).rjust(pad, '0')}{marker_type}" for i in range(list_len)]
    else:
        first_marker = f"{starting_number}{marker_type}"
        other_marker = "0" * (len(str(starting_number)) - 1) + "1" + marker_type
        markers = [first_marker] + [other_marker] * (list_len - 1)

    return _render_list(node, context, markers)


class ListsPlugin:
    """An mdformat plugin to configure list markers for unordered and ordered lists."""

    RENDERERS: Mapping[str, Render] = {"bullet_list": _bullet_list, "ordered_list": _ordered_list}

    @staticmethod
    def add_cli_argument_group(group: argparse._ArgumentGroup) -> None:
        group.add_argument(
            "--bullet",
            type=str,
            choices=VALID_BULLETS,
            default=DEFAULT_BULLET,
            help="Character to use for bullet list items (default: -)",
        )
        group.add_argument(
            "--ordered-marker",
            type=str,
            choices=VALID_ORDERED_MARKERS,
            default=DEFAULT_ORDERED_MARKER,
            help="Marker to use for ordered list items (default: .)",
        )

    @staticmethod
    def update_mdit(mdit: MarkdownIt) -> None:
        pass
