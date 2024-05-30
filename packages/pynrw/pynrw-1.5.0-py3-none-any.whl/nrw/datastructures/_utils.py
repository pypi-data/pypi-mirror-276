from __future__ import annotations

__all__: Final[list[str]] = ["display_binary_node"]

from typing import TYPE_CHECKING, Final, TypeVar

if TYPE_CHECKING:
    from nrw.datastructures._binary_search_tree import _BSTNode
    from nrw.datastructures._binary_tree import _BTNode
    from nrw.datastructures._comparable_content import ComparableContentT

_T = TypeVar("_T")


def display_binary_node(node: _BTNode[_T] | _BSTNode[ComparableContentT]) -> str:
    lines, *_ = _display_binary_node_impl(node)
    return "\n".join(lines[:-1])


def _display_binary_node_impl(  # pylint: disable=R0914
    node: _BTNode[_T] | _BSTNode[ComparableContentT] | None,
) -> tuple[list[str], int, int, int]:
    """Inspired by joowani.

    https://github.com/joowani/binarytree/blob/74e0c0bf204a0a2789c45a07264718f963db37fe/binarytree/__init__.py#L1891-L1981
    """
    if node is None:
        return [], 0, 0, 0

    line1: list[str] = []
    line2: list[str] = []
    node_repr: str = str(node._content)

    new_root_width = gap_size = len(node_repr)

    l_box, l_box_width, l_root_start, l_root_end = _display_binary_node_impl(
        node._left._node,
    )
    r_box, r_box_width, r_root_start, r_root_end = _display_binary_node_impl(
        node._right._node,
    )

    if l_box_width > 0:
        l_root: int = (l_root_start + l_root_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (l_box_width - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (l_box_width - l_root))
        new_root_start: int = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    line1.append(node_repr)
    line2.append(" " * new_root_width)

    if r_box_width > 0:
        r_root: int = (r_root_start + r_root_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (r_box_width - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (r_box_width - r_root))
        gap_size += 1
    new_root_end: int = new_root_start + new_root_width - 1

    gap: str = " " * gap_size
    new_box: list[str] = ["".join(line1), "".join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line: str = l_box[i] if i < len(l_box) else " " * l_box_width
        r_line: str = r_box[i] if i < len(r_box) else " " * r_box_width
        new_box.append(l_line + gap + r_line)

    return new_box, len(new_box[0]), new_root_start, new_root_end
