#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export course-paper evidence from the current research-hotspots project.

Outputs:
- field_counts.csv: paper/hotspot/topic counts by field
- social_science_hotspots.csv: top hotspots for Public Administration / Sociology / Political Science
- bertopic_vs_lda_summary.txt: compact summary from evaluate_results.json if present
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pymysql

from config import DB_CONF


PROJECT_ROOT = Path(__file__).resolve().parent
OUT_DIR = PROJECT_ROOT / "data" / "exports" / "course_evidence"


def connect():
    return pymysql.connect(**DB_CONF)


def fetch_rows(sql: str, params: tuple = ()) -> list[tuple]:
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def write_csv(path: Path, header: list[str], rows: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def export_field_counts() -> Path:
    rows = fetch_rows(
        """
        SELECT field,
               COUNT(*) AS paper_count,
               SUM(CASE WHEN abstract IS NOT NULL AND TRIM(abstract) <> '' THEN 1 ELSE 0 END) AS valid_papers
        FROM papers
        GROUP BY field
        ORDER BY field
        """
    )
    counts = []
    for field, paper_count, valid_papers in rows:
        hotspot_count = fetch_rows(
            "SELECT COUNT(*) FROM hotspots WHERE field = %s",
            (field,),
        )[0][0]
        topic_count = fetch_rows(
            "SELECT COUNT(*) FROM paper_topics WHERE field = %s",
            (field,),
        )[0][0]
        counts.append((field, paper_count, valid_papers, hotspot_count, topic_count))
    out = OUT_DIR / "field_counts.csv"
    write_csv(out, ["field", "papers", "valid_papers", "hotspots", "paper_topics"], counts)
    return out


def export_social_hotspots() -> Path:
    rows = fetch_rows(
        """
        SELECT field, topic_id, topic_label, paper_count, trend_status, title_cn, summary_cn
        FROM hotspots
        WHERE field IN ('Public Administration', 'Sociology', 'Political Science')
        ORDER BY field, paper_count DESC, topic_id
        """
    )
    out = OUT_DIR / "social_science_hotspots.csv"
    write_csv(
        out,
        ["field", "topic_id", "topic_label", "paper_count", "trend_status", "title_cn", "summary_cn"],
        rows,
    )
    return out


def export_bertopic_lda_summary() -> Path:
    results_path = PROJECT_ROOT / "evaluate_results.json"
    out = OUT_DIR / "bertopic_vs_lda_summary.txt"
    if not results_path.exists():
        out.write_text("evaluate_results.json not found.\n", encoding="utf-8")
        return out

    data = json.loads(results_path.read_text(encoding="utf-8"))
    bertopic_npmi = sum(item["BERTopic"]["NPMI"] for item in data) / len(data)
    lda_npmi = sum(item["LDA"]["NPMI"] for item in data) / len(data)
    bertopic_cov = sum(item["BERTopic"]["Coverage"] for item in data) / len(data)
    lda_cov = sum(item["LDA"]["Coverage"] for item in data) / len(data)
    bertopic_sil = sum(item["BERTopic"]["Silhouette"] for item in data) / len(data)
    lda_sil = sum(item["LDA"]["Silhouette"] for item in data) / len(data)

    lines = [
        "BERTopic vs LDA summary",
        f"fields: {len(data)}",
        f"avg_NPMI: BERTopic={bertopic_npmi:.4f}, LDA={lda_npmi:.4f}",
        f"avg_Coverage: BERTopic={bertopic_cov:.4f}, LDA={lda_cov:.4f}",
        f"avg_Silhouette: BERTopic={bertopic_sil:.4f}, LDA={lda_sil:.4f}",
        "",
        "Note: the comparison is mixed. BERTopic is not strictly better on every metric.",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [
        export_field_counts(),
        export_social_hotspots(),
        export_bertopic_lda_summary(),
    ]
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
