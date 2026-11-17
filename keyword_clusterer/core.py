import csv
import re
from collections import defaultdict
from pathlib import Path

STOPWORDS = {"a", "an", "the", "for", "of", "and", "to", "in", "on"}
INTENT_PATTERNS = [
    ("price", r"\b(price|prices|cost|costs|pricing)\b"),
    ("nutrition", r"\b(calorie|calories|nutrition|protein|carbs)\b"),
    ("hours", r"\b(hours|opening|closing|open|closed)\b"),
    ("location", r"\b(near me|location|locations|address|directions)\b"),
    ("recipe", r"\b(recipe|recipes|how to make)\b"),
    ("review", r"\b(review|reviews|rating|ratings)\b"),
]

def normalize(keyword):
    """Normalize text for deterministic grouping."""
    return " ".join(re.findall(r"[a-z0-9]+", keyword.lower()))

def intent(keyword):
    text = normalize(keyword)
    for label, pattern in INTENT_PATTERNS:
        if re.search(pattern, text):
            return label
    return "general"

def signature(keyword):
    """Group keywords with matching token sets and the same rule-based intent."""
    text = normalize(keyword)
    category = intent(keyword)
    tokens = set(text.split()) - STOPWORDS
    # Remove equivalent modifiers only within their own intent.
    equivalents = {
        "price": {"price", "prices", "cost", "costs", "pricing"},
        "nutrition": {"calorie", "calories", "nutrition", "protein", "carbs"},
        "hours": {"hours", "opening", "closing", "open", "closed"},
        "review": {"review", "reviews", "rating", "ratings"},
        "recipe": {"recipe", "recipes"},
    }
    tokens -= equivalents.get(category, set())
    return category, tuple(sorted(tokens))

def read_keywords(path):
    """Read CSV with keyword and optional volume columns."""
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "keyword" not in [x.strip().lower() for x in reader.fieldnames]:
            raise ValueError("Input CSV must contain a 'keyword' column")
        columns = {name.strip().lower(): name for name in reader.fieldnames}
        for row_number, row in enumerate(reader, start=2):
            keyword = (row.get(columns["keyword"]) or "").strip()
            if not keyword:
                continue
            raw_volume = (row.get(columns["volume"]) or "0").strip() if "volume" in columns else "0"
            try:
                volume = int(raw_volume.replace(",", ""))
                if volume < 0:
                    raise ValueError()
            except ValueError:
                raise ValueError(f"Invalid volume on CSV row {row_number}: {raw_volume!r}") from None
            yield {"keyword": keyword, "volume": volume}

def cluster(rows):
    """Return clusters sorted by highest-volume representative."""
    deduped = {}
    for row in rows:
        key = normalize(row["keyword"])
        if not key:
            continue
        if key not in deduped or row["volume"] > deduped[key]["volume"]:
            deduped[key] = row
    groups = defaultdict(list)
    for row in deduped.values():
        groups[signature(row["keyword"])].append(row)
    ordered = []
    for members in groups.values():
        members.sort(key=lambda item: (-item["volume"], item["keyword"].lower()))
        ordered.append(members)
    ordered.sort(key=lambda members: (-members[0]["volume"], members[0]["keyword"].lower()))
    result = []
    for number, members in enumerate(ordered, start=1):
        for row in members:
            result.append({
                "group_id": number,
                "main_keyword": members[0]["keyword"],
                "intent": intent(row["keyword"]),
                **row,
            })
    return result

def write_clusters(rows, path):
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["group_id", "main_keyword", "intent", "keyword", "volume"])
        writer.writeheader()
        writer.writerows(rows)
