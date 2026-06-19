# -*- coding: utf-8 -*-
"""
BERTopic vs LDA 定量对比评估引擎（~530 行）

在同一数据集上运行 BERTopic（复用 chuli2.py 超参数）与 sklearn LDA，
计算 NPMI、Diversity、Coverage、Silhouette 四项指标，输出终端对比表。

用法:
    python evaluate.py                              # 评估全部领域，默认保存到脚本同目录 evaluate_results.json
    python evaluate.py --fields "Medical Imaging"   # 指定单个领域
    python evaluate.py --output results.json        # 导出 JSON 到指定路径
    python evaluate.py --fields "Medical Imaging" "Statistics" --output results.json
    python evaluate.py --recompute-bertopic         # 不复用数据库，重新训练 BERTopic
"""

import argparse
import json
import re
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import silhouette_score
import nltk
from nltk.corpus import stopwords
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
from config import get_db_pool, FIELDS


# ================= 1. 文本清洗（复用 chuli2.py 配置） =================
try:
    english_stops = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    english_stops = set(stopwords.words("english"))

custom_stops = {
    "abstract", "study", "research", "results", "paper", "method",
    "proposed", "using", "based", "analysis", "approach", "data"
}


def clean_text(text: str) -> str:
    """针对学术文本的深度清洗，与 chuli2.py 完全一致"""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in english_stops and t not in custom_stops and len(t) > 2]
    return " ".join(tokens)


# ================= 2. 主题模型评估器 =================

class TopicModelEvaluator:
    """封装完整评估流水线，BERTopic 超参数与 chuli2.py 完全一致"""

    def __init__(self, recompute_bertopic: bool = False):
        self.recompute_bertopic = recompute_bertopic
        if not recompute_bertopic:
            self.embedding_model = None
            self.umap_model = None
            self.hdbscan_model = None
            return

        from bertopic import BERTopic
        from hdbscan import HDBSCAN
        from sentence_transformers import SentenceTransformer
        from umap import UMAP

        self.BERTopic = BERTopic

        # ---------- 与 chuli2.py 完全一致的 BERTopic 超参数 ----------
        self.embedding_model = SentenceTransformer("all-mpnet-base-v2")
        self.umap_model = UMAP(
            n_neighbors=15,
            n_components=3,
            min_dist=0.0,
            metric="cosine",
            random_state=42,
        )
        self.hdbscan_model = HDBSCAN(
            min_cluster_size=10,
            metric="euclidean",
            cluster_selection_method="eom",
        )

    # ---------- 数据加载 ----------

    def load_field_data(self, field: str) -> pd.DataFrame | None:
        """从数据库加载指定领域的论文并清洗"""
        conn = get_db_pool().connection()
        try:
            sql = (
                "SELECT id, title, abstract, year "
                "FROM papers WHERE field = %s AND abstract IS NOT NULL"
            )
            df = pd.read_sql(sql, conn, params=[field])
            if len(df) < 50:
                return None
            df["clean_text"] = (
                df["title"].fillna("") + ". " + df["abstract"].fillna("")
            ).apply(clean_text)
            df = df[df["clean_text"].str.len() > 30].reset_index(drop=True)
            return df
        finally:
            conn.close()

    # ---------- BERTopic ----------

    def run_bertopic(self, docs: list) -> tuple:
        """运行 BERTopic，产出主题分配 + 3D 坐标"""
        topic_model = self.BERTopic(
            embedding_model=self.embedding_model,
            umap_model=self.umap_model,
            hdbscan_model=self.hdbscan_model,
            nr_topics="auto",
            verbose=False,
        )
        topics, probs = topic_model.fit_transform(docs)
        reduced_embeddings = topic_model.umap_model.embedding_
        return topic_model, topics, probs, reduced_embeddings

    def load_stored_bertopic_result(self, field: str, df: pd.DataFrame) -> tuple:
        """Load BERTopic labels/coordinates already written by chuli2.py."""
        conn = get_db_pool().connection()
        try:
            pt_sql = (
                "SELECT paper_id, topic_id, x, y, z "
                "FROM paper_topics WHERE field = %s"
            )
            pt_df = pd.read_sql(pt_sql, conn, params=[field])

            h_sql = "SELECT topic_id, keywords FROM hotspots WHERE field = %s"
            h_df = pd.read_sql(h_sql, conn, params=[field])
        finally:
            conn.close()

        if pt_df.empty or h_df.empty:
            raise ValueError("stored BERTopic result not found in paper_topics/hotspots")

        topic_by_pid = {}
        coord_by_pid = {}
        for row in pt_df.itertuples(index=False):
            pid = str(row.paper_id)
            topic_by_pid[pid] = int(row.topic_id)
            coord_by_pid[pid] = (
                float(row.x or 0.0),
                float(row.y or 0.0),
                float(row.z or 0.0),
            )

        topics = []
        embeddings = []
        for row in df.itertuples(index=False):
            pid = str(row.id)
            topic_id = topic_by_pid.get(pid, -1)
            topics.append(topic_id)
            embeddings.append(coord_by_pid.get(pid, (0.0, 0.0, 0.0)))

        present_topic_ids = set(topics) - {-1}
        if not present_topic_ids:
            raise ValueError("stored BERTopic result has no non-noise documents")

        keywords_by_topic = {}
        for row in h_df.itertuples(index=False):
            topic_id = int(row.topic_id)
            if topic_id not in present_topic_ids:
                continue
            raw_keywords = row.keywords
            try:
                words = json.loads(raw_keywords) if isinstance(raw_keywords, str) else raw_keywords
            except Exception:
                words = []
            if isinstance(words, list):
                keywords_by_topic[topic_id] = [
                    str(w) for w in words[:10] if str(w).strip()
                ]

        bertopic_keywords = [
            keywords_by_topic[tid]
            for tid in sorted(present_topic_ids)
            if keywords_by_topic.get(tid)
        ]
        if not bertopic_keywords:
            raise ValueError("stored BERTopic keywords not found in hotspots.keywords")

        return topics, np.array(embeddings), bertopic_keywords

    # ---------- LDA ----------

    def run_lda(self, docs: list, n_topics: int) -> tuple:
        """运行 sklearn LDA，主题数对齐 BERTopic 有效主题数"""
        vectorizer = CountVectorizer(max_df=0.85, min_df=2, stop_words="english")
        dtm = vectorizer.fit_transform(docs)
        lda = LatentDirichletAllocation(
            n_components=max(n_topics, 2),
            random_state=42,
            max_iter=100,
            learning_method="online",
        )
        doc_topic_dist = lda.fit_transform(dtm)
        doc_topics = doc_topic_dist.argmax(axis=1)
        return lda, vectorizer, dtm, doc_topic_dist, doc_topics

    # ---------- 评估指标 ----------

    @staticmethod
    def compute_npmi(topics_keywords: list, docs_tokenized: list) -> float:
        """NPMI（c_npmi）— 主题模型评估金标准"""
        dictionary = Dictionary(docs_tokenized)
        dictionary.filter_extremes(no_below=2, no_above=0.85)
        cm = CoherenceModel(
            topics=topics_keywords,
            texts=docs_tokenized,
            dictionary=dictionary,
            coherence="c_npmi",
        )
        return cm.get_coherence()

    @staticmethod
    def compute_diversity(topics_keywords: list) -> float:
        """主题多样性：各主题 Top-N 词中唯一词占比"""
        all_words = [w for topic in topics_keywords for w in topic]
        unique_words = set(all_words)
        return len(unique_words) / len(all_words) if all_words else 0.0

    @staticmethod
    def compute_bertopic_coverage(topics: list) -> float:
        """BERTopic 覆盖度：非噪声文档比例"""
        non_noise = sum(1 for t in topics if t != -1)
        return non_noise / len(topics) if topics else 0.0

    @staticmethod
    def compute_lda_coverage(doc_topic_dist: np.ndarray, threshold: float = 0.2) -> float:
        """LDA 覆盖度：最大主题概率 > threshold 的文档比例"""
        max_probs = doc_topic_dist.max(axis=1)
        covered = sum(1 for p in max_probs if p > threshold)
        return covered / len(doc_topic_dist) if len(doc_topic_dist) > 0 else 0.0

    @staticmethod
    def compute_silhouette(embeddings: np.ndarray, labels: list) -> float:
        """轮廓系数 — 排除噪声点后计算"""
        labels_arr = np.array(labels)
        mask = labels_arr != -1
        if mask.sum() < 2 or len(set(labels_arr[mask])) < 2:
            return 0.0
        return silhouette_score(embeddings[mask], labels_arr[mask])

    # ---------- 关键词提取 ----------

    @staticmethod
    def extract_bertopic_keywords(topic_model, n_words: int = 10) -> list:
        """提取 BERTopic 各主题 Top-N 关键词"""
        result = []
        for tid, words in sorted(topic_model.get_topics().items()):
            if tid == -1:
                continue
            result.append([w for w, _ in words[:n_words]])
        return result

    @staticmethod
    def extract_lda_keywords(lda, vectorizer, n_words: int = 10) -> list:
        """提取 LDA 各主题 Top-N 关键词"""
        feature_names = vectorizer.get_feature_names_out()
        result = []
        for topic_idx in range(lda.n_components):
            top_features = lda.components_[topic_idx].argsort()[:-n_words - 1:-1]
            result.append([feature_names[i] for i in top_features])
        return result

    @staticmethod
    def _tokenize_docs(docs: list) -> list:
        """文档分词（用于 gensim CoherenceModel）"""
        return [d.split() for d in docs]

    # ---------- 单领域评估 ----------

    def evaluate_field(self, field: str) -> dict | None:
        """对单个领域执行完整评估"""
        print(f"\n{'=' * 60}")
        print(f"  评估领域: {field}")
        print(f"{'=' * 60}")

        df = self.load_field_data(field)
        if df is None:
            print(f"  ⚠️  数据不足 (<50 篇)，跳过")
            return None

        docs = df["clean_text"].tolist()
        docs_tokenized = self._tokenize_docs(docs)
        print(f"  文档数: {len(docs)}")

        # ---- BERTopic ----
        if self.recompute_bertopic:
            print("  [1/2] 重新运行 BERTopic...")
            topic_model, topics, probs, embeddings = self.run_bertopic(docs)
            bertopic_keywords = self.extract_bertopic_keywords(topic_model)
            bertopic_source = "recomputed"
        else:
            print("  [1/2] 从数据库读取已保存的 BERTopic 结果...")
            topics, embeddings, bertopic_keywords = self.load_stored_bertopic_result(field, df)
            bertopic_source = "stored_db"

        n_bertopic_topics = len(set(topics) - {-1})
        print(f"    BERTopic来源: {bertopic_source}; 有效主题数: {n_bertopic_topics}; "
              f"噪声: {sum(1 for t in topics if t == -1)}")

        # ---- LDA ----
        print("  [2/2] 运行 LDA (主题数对齐)...")
        n_lda_topics = max(n_bertopic_topics, 2)
        lda, vectorizer, dtm, doc_topic_dist, lda_topics = self.run_lda(docs, n_lda_topics)
        lda_keywords = self.extract_lda_keywords(lda, vectorizer)

        # ---- 计算指标 ----
        print("  计算评估指标...")

        bertopic_npmi = self.compute_npmi(bertopic_keywords, docs_tokenized)
        lda_npmi = self.compute_npmi(lda_keywords, docs_tokenized)

        bertopic_div = self.compute_diversity(bertopic_keywords)
        lda_div = self.compute_diversity(lda_keywords)

        bertopic_cov = self.compute_bertopic_coverage(topics)
        lda_cov = self.compute_lda_coverage(doc_topic_dist)

        bertopic_sil = self.compute_silhouette(embeddings, topics)
        lda_sil = self.compute_silhouette(doc_topic_dist, lda_topics)

        result = {
            "field": field,
            "n_docs": len(docs),
            "n_topics_bertopic": n_bertopic_topics,
            "n_topics_lda": n_lda_topics,
            "bertopic_source": bertopic_source,
            "BERTopic": {
                "NPMI": round(bertopic_npmi, 4),
                "Diversity": round(bertopic_div, 4),
                "Coverage": round(bertopic_cov, 4),
                "Silhouette": round(bertopic_sil, 4),
            },
            "LDA": {
                "NPMI": round(lda_npmi, 4),
                "Diversity": round(lda_div, 4),
                "Coverage": round(lda_cov, 4),
                "Silhouette": round(lda_sil, 4),
            },
        }

        # 打印单领域结果
        self._print_single_result(result)
        return result

    @staticmethod
    def _print_single_result(r: dict):
        """打印单个领域的对比结果"""
        b, l = r["BERTopic"], r["LDA"]
        h = "─"  # 水平线
        print(f"\n  ┌{h * 12}┬{h * 10}┬{h * 10}┐")
        print(f"  │ 指标{'':>8}│ BERTopic{'':>2}│ LDA{'':>6}│")
        print(f"  ├{h * 12}┼{h * 10}┼{h * 10}┤")
        print(f"  │ NPMI     │ {b['NPMI']:>8.4f} │ {l['NPMI']:>8.4f} │")
        print(f"  │ Diversity│ {b['Diversity']:>8.4f} │ {l['Diversity']:>8.4f} │")
        print(f"  │ Coverage │ {b['Coverage']:>8.4f} │ {l['Coverage']:>8.4f} │")
        print(f"  │ Silhouette│ {b['Silhouette']:>8.4f} │ {l['Silhouette']:>8.4f} │")
        print(f"  └{h * 12}┴{h * 10}┴{h * 10}┘")

    # ---------- 汇总输出 ----------

    @staticmethod
    def print_comparison_table(results: list) -> dict | None:
        """终端 ASCII 对比表，返回平均值"""
        if not results:
            return None

        print("\n" + "=" * 130)
        print("  BERTopic vs LDA 跨领域定量对比")
        print("=" * 130)

        header = (
            f"{'领域':<25} | {'文档数':>6} | {'主题数':>5} | "
            f"{'NPMI(B)':>8} | {'NPMI(L)':>8} | "
            f"{'Div(B)':>7} | {'Div(L)':>7} | "
            f"{'Cov(B)':>7} | {'Cov(L)':>7} | "
            f"{'Sil(B)':>7} | {'Sil(L)':>6}"
        )
        sep = "-" * 130

        print(header)
        print(sep)

        for r in results:
            b, l = r["BERTopic"], r["LDA"]
            print(
                f"{r['field']:<25} | {r['n_docs']:>6} | {r['n_topics_bertopic']:>5} | "
                f"{b['NPMI']:>8.4f} | {l['NPMI']:>8.4f} | "
                f"{b['Diversity']:>7.4f} | {l['Diversity']:>7.4f} | "
                f"{b['Coverage']:>7.4f} | {l['Coverage']:>7.4f} | "
                f"{b['Silhouette']:>7.4f} | {l['Silhouette']:>6.4f}"
            )

        print(sep)

        # 平均值行
        avg = {
            "BERTopic": {k: np.mean([r["BERTopic"][k] for r in results])
                         for k in ["NPMI", "Diversity", "Coverage", "Silhouette"]},
            "LDA": {k: np.mean([r["LDA"][k] for r in results])
                    for k in ["NPMI", "Diversity", "Coverage", "Silhouette"]},
        }
        print(
            f"{'平均':<25} | {'':>6} | {'':>5} | "
            f"{avg['BERTopic']['NPMI']:>8.4f} | {avg['LDA']['NPMI']:>8.4f} | "
            f"{avg['BERTopic']['Diversity']:>7.4f} | {avg['LDA']['Diversity']:>7.4f} | "
            f"{avg['BERTopic']['Coverage']:>7.4f} | {avg['LDA']['Coverage']:>7.4f} | "
            f"{avg['BERTopic']['Silhouette']:>7.4f} | {avg['LDA']['Silhouette']:>6.4f}"
        )

        return avg

    @staticmethod
    def print_summary_stem_vs_social(results: list):
        """STEM vs 社科分组平均对比，直接回应"社科迁移是否验证"审稿意见"""
        stem_fields = {
            "Artificial Intelligence", "Quantum Physics", "Computational Biology",
            "Econometrics", "Astrophysics", "Statistics", "Condensed Matter",
            "High Energy Physics", "Algebraic Geometry", "Medical Imaging",
        }
        social_fields = {"Public Administration", "Sociology", "Political Science"}

        stem_results = [r for r in results if r["field"] in stem_fields]
        social_results = [r for r in results if r["field"] in social_fields]

        if not stem_results or not social_results:
            print("\n  ⚠️  无法计算分组对比：STEM 或社科领域数据不足")
            return

        print("\n" + "=" * 100)
        print("  STEM vs 社科 分组平均对比")
        print("=" * 100)

        def group_avg(group):
            return {
                "BERTopic": {k: np.mean([r["BERTopic"][k] for r in group])
                             for k in ["NPMI", "Diversity", "Coverage", "Silhouette"]},
                "LDA": {k: np.mean([r["LDA"][k] for r in group])
                        for k in ["NPMI", "Diversity", "Coverage", "Silhouette"]},
            }

        stem_avg = group_avg(stem_results)
        social_avg = group_avg(social_results)

        header = (
            f"{'分组':<12} | {'':>8} | "
            f"{'NPMI(B)':>8} | {'NPMI(L)':>8} | "
            f"{'Div(B)':>7} | {'Div(L)':>7} | "
            f"{'Cov(B)':>7} | {'Cov(L)':>7} | "
            f"{'Sil(B)':>7} | {'Sil(L)':>6}"
        )
        sep = "-" * 100
        print(header)
        print(sep)

        for label, avg_data in [("STEM", stem_avg), ("社科", social_avg)]:
            b, l = avg_data["BERTopic"], avg_data["LDA"]
            print(
                f"{label:<12} | {'':>8} | "
                f"{b['NPMI']:>8.4f} | {l['NPMI']:>8.4f} | "
                f"{b['Diversity']:>7.4f} | {l['Diversity']:>7.4f} | "
                f"{b['Coverage']:>7.4f} | {l['Coverage']:>7.4f} | "
                f"{b['Silhouette']:>7.4f} | {l['Silhouette']:>6.4f}"
            )

        print(sep)

        # 差值（STEM - 社科）
        diff = {
            "BERTopic": {k: stem_avg["BERTopic"][k] - social_avg["BERTopic"][k]
                         for k in ["NPMI", "Diversity", "Coverage", "Silhouette"]},
            "LDA": {k: stem_avg["LDA"][k] - social_avg["LDA"][k]
                    for k in ["NPMI", "Diversity", "Coverage", "Silhouette"]},
        }
        db, dl = diff["BERTopic"], diff["LDA"]
        print(
            f"{'差值(STEM-社科)':<12} | {'':>8} | "
            f"{db['NPMI']:>+8.4f} | {dl['NPMI']:>+8.4f} | "
            f"{db['Diversity']:>+7.4f} | {dl['Diversity']:>+7.4f} | "
            f"{db['Coverage']:>+7.4f} | {dl['Coverage']:>+7.4f} | "
            f"{db['Silhouette']:>+7.4f} | {dl['Silhouette']:>+6.4f}"
        )

        print(f"\n  STEM 领域数: {len(stem_results)} | "
              f"社科领域数: {len(social_results)}")

    # ---------- 全流水线 ----------

    def run_all(self, fields: list = None, output: str = None) -> list:
        """运行完整评估流水线"""
        target_fields = fields or FIELDS
        print("BERTopic vs LDA 定量对比评估")
        print(f"目标领域: {', '.join(target_fields)}")

        results = []
        for field in target_fields:
            try:
                result = self.evaluate_field(field)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"  ❌ [{field}] 评估失败: {e}")

        if len(results) >= 2:
            self.print_comparison_table(results)
            self.print_summary_stem_vs_social(results)

        if output and results:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n  📄 结果已导出至: {output}")

        return results


# ================= 3. CLI 入口 =================

def main():
    parser = argparse.ArgumentParser(
        description="BERTopic vs LDA 定量对比评估"
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        default=None,
        help="指定评估领域 (默认: config.FIELDS 全部)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="JSON 导出路径；默认保存到脚本同目录的 evaluate_results.json",
    )
    parser.add_argument(
        "--recompute-bertopic",
        action="store_true",
        help="重新训练 BERTopic；默认读取 chuli2.py 已写入数据库的 paper_topics/hotspots",
    )
    args = parser.parse_args()

    output = args.output or str(Path(__file__).resolve().with_name("evaluate_results.json"))
    evaluator = TopicModelEvaluator(recompute_bertopic=args.recompute_bertopic)
    evaluator.run_all(fields=args.fields, output=output)


if __name__ == "__main__":
    main()
