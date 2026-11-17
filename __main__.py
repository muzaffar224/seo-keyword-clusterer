import argparse
from .core import cluster, read_keywords, write_clusters

def main():
    parser = argparse.ArgumentParser(description="Offline rule-based SEO keyword clustering")
    parser.add_argument("input", help="CSV with keyword and optional volume columns")
    parser.add_argument("output", help="Destination CSV")
    args = parser.parse_args()
    rows = cluster(read_keywords(args.input))
    write_clusters(rows, args.output)
    print(f"Exported {len(rows)} keywords across {len(set(row['group_id'] for row in rows))} groups to {args.output}")

if __name__ == "__main__":
    main()
