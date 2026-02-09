#!/usr/bin/env python3
"""
Initialize a new literature review folder structure.

Usage:
    python init_review.py --project PATH --topic TOPIC_SLUG
    python init_review.py --project PATH --topic TOPIC_SLUG --date 2026-01-15

Creates:
    Literature/
        INDEX.md          (from template, if not exists)
        YYYY-MM-DD_topic-slug/
            REVIEW_PROGRESS.md  (from template)
            Full_text_references/

Reads templates from the skill's templates/ directory rather than
embedding template content (fixes R-2 template duplication).
"""

import argparse
import sys
from datetime import date
from pathlib import Path


def get_template_dir():
    """Resolve the templates directory relative to this script."""
    return Path(__file__).resolve().parent.parent / "templates"


def read_template(name):
    """Read a template file and return its contents."""
    template_path = get_template_dir() / name
    if not template_path.exists():
        print(f"Error: Template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")


def fill_template(content, replacements):
    """Replace {{PLACEHOLDER}} tokens in template content."""
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def init_review(project_path, topic_slug, review_date=None):
    """Initialize a new literature review folder structure."""
    project = Path(project_path).resolve()
    if not project.exists():
        print(f"Error: Project path does not exist: {project}", file=sys.stderr)
        sys.exit(1)

    if review_date is None:
        review_date = date.today().isoformat()

    lit_dir = project / "Literature"
    review_dir = lit_dir / f"{review_date}_{topic_slug}"
    full_text_dir = review_dir / "Full_text_references"

    # Create directories
    review_dir.mkdir(parents=True, exist_ok=True)
    full_text_dir.mkdir(exist_ok=True)

    # Create INDEX.md if it does not exist
    index_path = lit_dir / "INDEX.md"
    if not index_path.exists():
        index_content = read_template("INDEX.md")
        index_path.write_text(index_content, encoding="utf-8")
        print(f"Created: {index_path}")
    else:
        print(f"Exists:  {index_path}")

    # Create REVIEW_PROGRESS.md from template
    progress_path = review_dir / "REVIEW_PROGRESS.md"
    if progress_path.exists():
        print(f"Warning: {progress_path} already exists. Skipping.")
    else:
        progress_content = read_template("REVIEW_PROGRESS.md")
        replacements = {
            "DATE": review_date,
            "TOPIC": topic_slug.replace("-", " ").title(),
        }
        progress_content = fill_template(progress_content, replacements)
        progress_path.write_text(progress_content, encoding="utf-8")
        print(f"Created: {progress_path}")

    print(f"\nReview folder ready: {review_dir}")
    print(f"Next: Update INDEX.md with this review's row.")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new literature review folder structure."
    )
    parser.add_argument(
        "--project", required=True, help="Path to the project root directory"
    )
    parser.add_argument(
        "--topic", required=True, help="Topic slug (e.g., 'rtm-adjustment-methods')"
    )
    parser.add_argument(
        "--date", default=None, help="Review date (YYYY-MM-DD). Defaults to today."
    )
    args = parser.parse_args()
    init_review(args.project, args.topic, args.date)


if __name__ == "__main__":
    main()
