#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re


class PatternAnalyzer:
    def __init__(self):
        self.PATTERNS_DIR = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "patterns"
        )
        self.patterns_cache = {}

    def get_pattern(self, pattern_name):
        """從快取或檔案載入一個 pattern，避免重複讀取"""
        if pattern_name in self.patterns_cache:
            return self.patterns_cache[pattern_name]

        pattern_file = os.path.join(self.PATTERNS_DIR, f"{pattern_name}.json")
        try:
            with open(pattern_file, "r") as f:
                pat_data = json.load(f)
                self.patterns_cache[pattern_name] = pat_data
                return pat_data
        except FileNotFoundError:
            raise ValueError(f"No such pattern '{pattern_name}'")
        except json.JSONDecodeError:
            raise ValueError(f"Pattern file '{pattern_file}' is malformed JSON.")

    def analyze(self, lines, pattern_name):
        """
        核心分析函式。它只負責一件事：拿著資料和規則去分析。
        它不關心資料是從哪來的。
        """
        pat_data = self.get_pattern(pattern_name)

        flags = pat_data.get("flags", "")
        pattern_str = pat_data.get("pattern")
        patterns = pat_data.get("patterns")

        if not pattern_str and patterns:
            pattern_str = f"({'|'.join(patterns)})"
        if not pattern_str:
            raise ValueError(
                f"Pattern file for '{pattern_name}' contains no pattern(s)."
            )

        re_flags = re.IGNORECASE if "i" in flags else 0

        try:
            compiled_pattern = re.compile(pattern_str, flags=re_flags)
        except re.error as e:
            raise ValueError(f"Invalid regex in '{pattern_name}.json': {e}")

        results = []
        only_match_mode = "o" in flags

        for line_num, line in enumerate(lines, 1):
            iterator = compiled_pattern.finditer(line)
            for match in iterator:
                results.append(
                    {
                        "line": line_num,
                        "match": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                    }
                )
                if not only_match_mode:
                    break

        return {
            "pattern": pattern_name,
            "matches": results,
            "count": len(results),
        }


def main():
    analyzer = PatternAnalyzer()

    parser = argparse.ArgumentParser(
        description="A Python-based analysis engine for text patterns."
    )
    parser.add_argument(
        "pattern_name", nargs="?", help="Pattern to use ('all' for all patterns)."
    )
    parser.add_argument(
        "target_path", nargs="?", help="Target file path (if not using a pipe)."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available patterns."
    )

    args = parser.parse_args()

    if args.list:
        try:
            patterns = sorted(
                [
                    p.replace(".json", "")
                    for p in os.listdir(analyzer.PATTERNS_DIR)
                    if p.endswith(".json")
                ]
            )
            for p in patterns:
                print(p)
        except FileNotFoundError:
            print(
                f"FUCK: Pattern directory not found at '{analyzer.PATTERNS_DIR}'",
                file=sys.stderr,
            )
            sys.exit(1)
        sys.exit(0)

    if not args.pattern_name:
        parser.print_help()
        sys.exit(1)

    # --- 這就是全新的 I/O 處理邏輯 ---
    lines = []
    input_source = "stdin"
    if not sys.stdin.isatty():
        lines = sys.stdin.readlines()
    elif args.target_path:
        input_source = args.target_path
        try:
            if os.path.isdir(input_source):
                print(
                    f"FUCK: '{input_source}' is a directory. Analysis engine needs a file.",
                    file=sys.stderr,
                )
                sys.exit(1)
            with open(input_source, "r", errors="ignore") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"FUCK: Target file not found at '{input_source}'", file=sys.stderr)
            sys.exit(1)
    else:
        print(
            "FUCK: No input data. Provide a file path or pipe data to stdin.",
            file=sys.stderr,
        )
        sys.exit(1)
    # --- 水已經打好，放在 `lines` 這個水桶裡了 ---

    final_results = {}
    try:
        if args.pattern_name.lower() == "all":
            all_patterns = sorted(
                [
                    p.replace(".json", "")
                    for p in os.listdir(analyzer.PATTERNS_DIR)
                    if p.endswith(".json")
                ]
            )
            analysis_results = [analyzer.analyze(lines, p) for p in all_patterns]
            final_results = {
                "source": input_source,
                "analysis": [
                    res for res in analysis_results if res["count"] > 0
                ],  # 只保留有結果的
            }
        else:
            final_results = analyzer.analyze(lines, args.pattern_name)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(final_results, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
