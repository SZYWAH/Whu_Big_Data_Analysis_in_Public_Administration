# Research Hotspots Project

This project builds a pipeline for academic text analysis:

1. crawl papers from arXiv and OpenAlex
2. clean and deduplicate data
3. run BERTopic topic discovery
4. generate Chinese hotspot names and reviews with DeepSeek
5. visualize results in Streamlit

## Main scripts

- `update_local_data.py`: full pipeline runner
- `chuli2.py`: BERTopic clustering and hotspot writing
- `namer.py`: hotspot naming
- `review5.py`: review generation
- `evaluate.py`: BERTopic vs LDA comparison
- `export_course_evidence.py`: export course-paper evidence tables
- `app17.py`: Streamlit UI

## Course-paper focus

The current database includes:

- `Public Administration`
- `Sociology`
- `Political Science`

These fields already have corresponding hotspots, names, and reviews in the database.

## Useful commands

```bash
python evaluate.py --output evaluate_results.json
python export_course_evidence.py
python update_local_data.py
streamlit run app17.py
```

## Notes

- `evaluate.py` compares BERTopic and LDA on the same field-level corpus.
- `export_course_evidence.py` writes CSV/TXT evidence into `data/exports/course_evidence/`.
- Environment variables take priority; `.env` is loaded only as a local fallback.
- `HF_ENDPOINT` can be configured through the environment or `.env` for Hugging Face downloads.
