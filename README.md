# SEO Keyword Clusterer

A free, offline Python command-line tool for **basic rule-based SEO keyword grouping**.

It reads a CSV file of keywords and optional search volumes, removes exact normalized duplicates, assigns simple intent categories, groups keywords with equivalent token sets, selects the highest-volume main keyword in each group, and exports the results as CSV.

**Important:** This is a deterministic starter tool, **not** an AI semantic clustering engine. It does not query search engines, compare SERPs, estimate search volumes, or guarantee matching search intent. Review every cluster manually before planning pages.

## Requirements

- Python 3.9+ (standard library only; no dependencies)

## Quick start

From the project directory:

```bash
python -m keyword_clusterer examples/keywords.csv clusters.csv
```

On some systems, use `python3` instead of `python`.

Input format:

```csv
keyword,volume
greggs price,1200
greggs cost,500
greggs calories,900
```

The `keyword` header is required. `volume` is optional; missing volumes default to zero. Volumes must be nonnegative integers. Output columns: `group_id`, `main_keyword`, `intent`, `keyword`, `volume`.

## How grouping works

- Text is lowercased and punctuation is normalized.
- Identical normalized keywords are deduplicated, retaining the highest-volume row.
- A few English modifier patterns assign intents: price, nutrition, hours, location, recipe, review, or general.
- Within each intent, keywords are grouped only if their remaining normalized token sets match.
- Groups and their keywords are sorted by descending volume.

This deliberately conservative method will miss many true semantic equivalents and may group some phrases incorrectly. It is English-focused; it does not handle stemming, multilingual search intent, geographic SERP variation, or ambiguous meanings.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports, tests, and improvements are welcome.

## License

MIT — see [LICENSE](LICENSE).
