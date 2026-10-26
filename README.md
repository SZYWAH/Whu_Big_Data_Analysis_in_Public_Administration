# 基于 NLP 与大语言模型的网络学术大数据分析框架

[GitHub 主页](https://github.com/SZYWAH) · [核心功能](#核心功能) · [科研热点桌面工作台](https://github.com/SZYWAH/research-hotspots-desktop)

本项目面向公共管理大数据课程论文场景，构建了一套网络学术大数据分析流程。系统从 arXiv 与 OpenAlex 获取论文数据，完成清洗去重、BERTopic 研究热点识别、LDA 方法对比、LLM 中文热点命名与综述生成，并通过 Streamlit 提供可视化交互界面。

## 项目概况

- 类型：公共管理大数据课程研究与方法实验。
- 技术栈：Python、Streamlit、MySQL、BERTopic、LDA 与 DeepSeek API。
- 交付方式：源码、实验流程与结果文件；当前未发布 GitHub Release。
- 相关项目：[research-hotspots-desktop](https://github.com/SZYWAH/research-hotspots-desktop) 面向本地桌面使用。本仓库保留课程研究、方法对比和多源采集流程。

## 项目定位

项目当前采用“13 个学科总体方法验证 + 公共管理相关三领域重点分析”的思路。arXiv 数据主要覆盖理工科领域，OpenAlex 用于扩展公共管理、社会学、政治学等社会科学数据。

公共管理课程论文重点关注：

- `Public Administration`
- `Sociology`
- `Political Science`

这三个领域已经在数据库中生成对应热点、中文命名和综述内容，可用于支撑论文中的公共管理相关案例分析。

## 核心功能

1. 多源学术数据采集：从 arXiv 与 OpenAlex 抓取论文元数据、摘要和年份信息。
2. 数据清洗与去重：清理无效摘要、重复 DOI、重复标题和异常文本。
3. 研究热点发现：使用 BERTopic 进行语义聚类，生成热点、关键词和三维坐标。
4. 方法对比评估：在同一数据集上比较 BERTopic 与 LDA 的 NPMI、覆盖率、主题多样性和分离指标。
5. LLM 辅助生成：调用 DeepSeek 接口生成中文热点名称、摘要描述和领域综述。
6. 课程论文证据导出：导出字段统计、社会科学热点表和 BERTopic/LDA 对比摘要。
7. 可视化展示：使用 Streamlit 展示热点、论文、星图和综述生成结果。

## 主要脚本

- `update_local_data.py`：完整流水线调度脚本。
- `arxiv_crawler.py`：arXiv 数据采集。
- `openalex_crawler.py`：OpenAlex 数据采集，当前重点采集公共管理相关社会科学领域。
- `cleaner.py`：数据库论文清洗与去重。
- `chuli2.py`：BERTopic 聚类、热点识别和三维坐标写入。
- `namer.py`：调用 LLM 生成热点中文名称与描述。
- `review5.py`：调用 LLM 生成热点综述。
- `evaluate.py`：BERTopic 与 LDA 定量对比。
- `export_course_evidence.py`：导出课程论文所需证据表。
- `app17.py`：Streamlit 可视化界面。

## 常用命令

```bash
python update_local_data.py
python evaluate.py --output evaluate_results.json
python export_course_evidence.py
streamlit run app17.py
```

## 配置说明

项目通过环境变量读取数据库、DeepSeek 和路径配置。真实环境变量优先，`.env` 只作为本地兜底配置文件使用，不应提交到 Git 仓库。

常用配置项包括：

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`
- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_MODEL_NAME`
- `HF_ENDPOINT`
- `EXPORT_DIR`

## 结果文件

- `evaluate_results.json`：BERTopic 与 LDA 的定量评估结果。
- `data/exports/course_evidence/field_counts.csv`：各学科论文数、热点数和入簇数统计。
- `data/exports/course_evidence/social_science_hotspots.csv`：公共管理、社会学、政治学三领域热点结果。
- `data/exports/course_evidence/bertopic_vs_lda_summary.txt`：方法对比摘要。

## 注意事项

- 当前项目不包含 `.env`、数据库文件和真实 API Key。
- BERTopic 并非在所有指标上绝对优于 LDA；本项目选择 BERTopic，主要因为它更适合发现可解释研究热点。
- LLM 综述生成重点覆盖公共管理、社会学、政治学三个公共管理相关领域，并不声称覆盖全部学科。
- 如果公开上传仓库，建议确认是否需要保留 `data/exports/` 下的生成报告和 `assets/fonts/` 下的字体文件。

