import typer as ty
from pathlib import Path
from typing import Optional
import json

from astchunk import ASTChunkBuilder

app = ty.Typer(help="AST-based code chunking CLI")


@app.command()
def chunk(
    input_file: Path = ty.Argument(
        ...,
        help="Input file containing source code to chunk",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    output_file: Optional[Path] = ty.Option(
        None,
        "-o",
        "--output",
        help="Output file for chunks (optional, prints to stdout if not specified)",
        file_okay=True,
        dir_okay=False,
    ),
    max_chunk_size: int = ty.Option(
        1800,
        "-m",
        "--max-chunk-size",
        help="Maximum non-whitespace characters per chunk",
    ),
    language: str = ty.Option(
        "python",
        "-l",
        "--language",
        help="Programming language (python, java, csharp, typescript)",
    ),
    metadata_template: str = ty.Option(
        "default",
        "-t",
        "--metadata-template",
        help="Metadata template to use",
    ),
    chunk_expansion: bool = ty.Option(
        False,
        "-e",
        "--chunk-expansion",
        help="Enable chunk expansion with metadata headers",
    ),
    chunk_overlap: int = ty.Option(
        450,
        "--chunk-overlap",
        help="Number of AST nodes to overlap between chunks",
    ),
    repo_name: Optional[str] = ty.Option(
        None,
        "--repo-name",
        help="Repository name for metadata",
    ),
    file_path: Optional[str] = ty.Option(
        None,
        "--file-path",
        help="File path for metadata",
    ),
    json_output: bool = ty.Option(
        False,
        "-j",
        "--json",
        help="Output as JSON instead of human-readable format",
    ),
):
    """
    Chunk source code into AST-based chunks.
    """
    code = input_file.read_text(encoding="utf-8")

    configs = {
        "max_chunk_size": max_chunk_size,
        "language": language,
        "metadata_template": metadata_template,
        "chunk_expansion": chunk_expansion,
        "chunk_overlap": chunk_overlap,
    }

    repo_level_metadata = {}
    if repo_name:
        repo_level_metadata["repo_name"] = repo_name
    if file_path:
        repo_level_metadata["file_path"] = file_path

    if repo_level_metadata:
        configs["repo_level_metadata"] = repo_level_metadata

    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(code, **configs)

    if json_output:
        output = json.dumps(chunks, indent=2)
        if output_file:
            output_file.write_text(output, encoding="utf-8")
            ty.echo(f"Wrote {len(chunks)} chunks to {output_file}")
        else:
            ty.echo(output)
    else:
        lines = []
        lines.append(
            f"AST Chunking Results (max {max_chunk_size} non-whitespace chars per chunk)"
        )
        lines.append("=" * 80)
        lines.append("")

        for i, chunk in enumerate(chunks, 1):
            content = chunk.get("content", chunk.get("context", ""))
            metadata = chunk.get("metadata", {})
            line_count = len(content.split("\n"))

            header = f"{'-' * 25} Chunk {i} ({line_count} lines / {metadata.get('chunk_size', 0)} chars) {'-' * 25}"
            lines.append(header)
            lines.append(content)
            lines.append("-" * (len(header)))
            lines.append("")

        output = "\n".join(lines)

        if output_file:
            output_file.write_text(output, encoding="utf-8")
            ty.echo(f"Wrote {len(chunks)} chunks to {output_file}")
        else:
            ty.echo(output)

    ty.echo(f"Created {len(chunks)} chunks")


if __name__ == "__main__":
    app()
