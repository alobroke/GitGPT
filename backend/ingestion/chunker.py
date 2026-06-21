import ast

MAX_CHARS = 4000


def get_source_segment(lines, node):
    start = node.lineno - 1
    end = node.end_lineno
    return "".join(lines[start:end])


def chunk_python_file(file_path):

    chunks = []

    try:

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        lines = source.splitlines(keepends=True)

        for node in tree.body:

            # -----------------------------
            # Top-Level Functions
            # -----------------------------
            if isinstance(node, ast.FunctionDef):

                content = get_source_segment(lines, node)

                if len(content) > MAX_CHARS:
                    content = content[:MAX_CHARS]

                chunk_id = (
                    f"{file_path}"
                    f"::function::{node.name}"
                )

                chunks.append({
                    "id": chunk_id,
                    "file": file_path,
                    "chunk_type": "function",
                    "name": node.name,
                    "start_line": node.lineno,
                    "end_line": node.end_lineno,
                    "content": content
                })

            # -----------------------------
            # Classes
            # -----------------------------
            elif isinstance(node, ast.ClassDef):

                class_name = node.name

                # Only store methods
                for child in node.body:

                    if not isinstance(
                        child,
                        ast.FunctionDef
                    ):
                        continue

                    # Skip dunder methods
                    if child.name.startswith("__"):
                        continue

                    content = get_source_segment(
                        lines,
                        child
                    )

                    if len(content) > MAX_CHARS:
                        content = content[:MAX_CHARS]

                    method_id = (
                        f"{file_path}"
                        f"::class::{class_name}"
                        f"::method::{child.name}"
                    )

                    chunks.append({
                        "id": method_id,
                        "file": file_path,
                        "chunk_type": "method",
                        "class_name": class_name,
                        "name": child.name,
                        "start_line": child.lineno,
                        "end_line": child.end_lineno,
                        "content": content
                    })

        return chunks

    except Exception as e:

        print(
            f"Error processing "
            f"{file_path}: {e}"
        )

        return []