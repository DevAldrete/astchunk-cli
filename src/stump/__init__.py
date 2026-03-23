"""
Stump — AST-based code chunking (tree-sitter).

Derived from ASTChunk (Yilin Zhang et al.); see NOTICE and README for attribution
and how to cite the cAST paper. Public API types keep their original names
(e.g. ``ASTChunk``, ``ASTChunkBuilder``) for compatibility with the upstream design.
"""

from .astchunk_builder import ASTChunkBuilder
from .astchunk import ASTChunk
from .astnode import ASTNode
from .symbols import DefinitionSpan, collect_definitions, symbols_overlapping_chunk
from .preprocessing import (
    ByteRange,
    IntRange,
    preprocess_nws_count,
    get_nws_count,
    get_nws_count_direct,
    get_nodes_in_brange,
    get_largest_node_in_brange
)

__version__ = "0.1.0"

__all__ = [
    "ASTChunkBuilder",
    "ASTChunk",
    "ASTNode",
    "DefinitionSpan",
    "collect_definitions",
    "symbols_overlapping_chunk",
    "ByteRange",
    "IntRange",
    "preprocess_nws_count",
    "get_nws_count",
    "get_nws_count_direct",
    "get_nodes_in_brange",
    "get_largest_node_in_brange"
]
