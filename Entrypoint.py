"""
entrypoint.py
GitGPT GitHub Action entrypoint.

GitHub Actions exposes `with:` inputs as environment variables named
INPUT_<NAME-WITH-DASHES-UPPERCASED>, e.g. `llm-provider` -> INPUT_LLM-PROVIDER.
Actions normalizes dashes to underscores is NOT guaranteed across all runners
for Docker actions, so we read both forms defensively.
"""

from __future__ import annotations

import json
import os
import sys

from github_client import extract_question, post_comment, load_event
from indexer import get_or_build_index, Reranker
from llm import get_backend


def _input(name: str, default: str = "") -> str:
    key_dash = f"INPUT_{name.upper()}"
    key_underscore = f"INPUT_{name.upper().replace('-', '_')}"
    return os.environ.get(key_dash) or os.environ.get(key_underscore) or default


def _bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes")


def set_output(name: str, value: str) -> None:
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if not gh_output:
        return
    # Multiline-safe output format
    delimiter = "GITGPT_EOF"
    with open(gh_output, "a", encoding="utf-8") as f:
        f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def main() -> int:
    question_input = _input("question") or (sys.argv[1] if len(sys.argv) > 1 else "")
    github_token = _input("github-token")
    llm_provider = _input("llm-provider", "anthropic")
    llm_model = _input("llm-model", "claude-sonnet-4-6")
    api_key = _input("api-key")
    embedding_model = _input("embedding-model", "BAAI/bge-small-en-v1.5")
    top_k = int(_input("top-k", "8") or 8)
    paths_raw = _input("paths", "**/*.py,**/*.js,**/*.ts,**/*.tsx,**/*.jsx,**/*.go,**/*.java,**/*.md")
    patterns = [p.strip() for p in paths_raw.split(",") if p.strip()]
    post_comment_flag = _bool(_input("post-comment", "true"))
    cache_index = _bool(_input("cache-index", "true"))

    question = extract_question(question_input)
    if not question:
        print(
            "::notice::No question found (no 'question' input and no "
            "'/gitgpt <question>' command detected in the triggering event). "
            "Nothing to do."
        )
        return 0

    workspace = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
    print(f"::group::Indexing repository at {workspace}")
    try:
        index = get_or_build_index(
            repo_root=workspace,
            embedding_model=embedding_model,
            patterns=patterns,
            use_cache=cache_index,
        )
    except Exception as exc:
        print(f"::error::Failed to build/load index: {exc}")
        return 1
    print(f"Indexed {len(index.chunks)} chunks.")
    print("::endgroup::")

    print(f"::group::Retrieving context for: {question}")
    candidates = index.search(question, top_k=top_k)
    reranker = Reranker()
    top_chunks = reranker.rerank(question, candidates, top_n=min(5, len(candidates)))
    print(f"Retrieved {len(top_chunks)} chunks after re-ranking.")
    print("::endgroup::")

    context_blocks = [
        f"File: {c.file_path} (lines {c.start_line}-{c.end_line})\n```\n{c.text}\n```"
        for c, _ in top_chunks
    ]
    sources = [f"{c.file_path}#L{c.start_line}-L{c.end_line}" for c, _ in top_chunks]

    print(f"::group::Generating answer via {llm_provider}:{llm_model}")
    try:
        backend = get_backend(llm_provider, llm_model, api_key)
        answer = backend.generate(question, context_blocks)
    except Exception as exc:
        print(f"::error::LLM generation failed: {exc}")
        return 1
    print("::endgroup::")

    print("\n=== GitGPT Answer ===\n")
    print(answer)
    print("\n=== Sources ===")
    for s in sources:
        print(f"- {s}")

    set_output("answer", answer)
    set_output("sources", json.dumps(sources))

    if post_comment_flag:
        event = load_event()
        repo_full_name = os.environ.get("GITHUB_REPOSITORY", "")
        has_target = "issue" in event or "pull_request" in event
        if github_token and repo_full_name and has_target:
            try:
                post_comment(github_token, repo_full_name, answer, sources)
                print("Posted answer as a comment.")
            except Exception as exc:
                print(f"::warning::Failed to post comment: {exc}")
        else:
            print(
                "::notice::Skipping comment post (no PR/issue context, e.g. "
                "this run was triggered via workflow_dispatch)."
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())