import collections as col
import string
from pathlib import Path


class TextProcessor:
    def __init__(self, stop_words: set[str] | None = None):
        if stop_words is not None:
            self.stop_words = stop_words
        else:
            self.stop_words = self._load_default_stop_words()

    def _load_default_stop_words(self) -> set[str]:
        stop_words_path = Path(__file__).resolve().parent / "stop_words.txt"

        try:
            with open(stop_words_path, "r", encoding="utf-8") as f:
                return set(f.read().split())
        except FileNotFoundError:
            return set()

    def normalize(self, text: str) -> str:
        clean_string = "".join(
            [
                char.lower() if char not in string.punctuation else " "
                for char in text.strip()
            ]
        )

        words = clean_string.split()
        result_text = [word for word in words if word not in self.stop_words]

        return " ".join(result_text)


class InvertedIndex:
    def __init__(self):
        self.processor = TextProcessor()
        self.index = col.defaultdict(set)

    def build_ngrams(self, word: str, n: int = 3) -> set[str]:
        if len(word) < n:
            return {f"_{word}_"}
        word = f"_{word}_"

        return {word[i : i + n] for i in range(len(word) - n + 1)}

    def build_index(
        self,
        documents: dict[int, dict],
        n: int = 3,
    ) -> dict[str, set[int]]:

        self.index.clear()

        for doc_id, doc_data in documents.items():
            text = f"{doc_data['title']} {doc_data['content']}"
            words = self.processor.normalize(text).split()
            for word in words:
                trigrams = self.build_ngrams(word, n)
                for trigram in trigrams:
                    self.index[trigram].add(doc_id)

        return dict(self.index)

    def search(self, query: str, n: int = 3) -> list[dict]:
        normal_query = self.processor.normalize(query)
        if not normal_query.strip():
            return []

        query_ngrams = set()
        for word in normal_query.split():
            query_ngrams.update(self.build_ngrams(word, n))

        scores = col.defaultdict(int)
        for tgram in query_ngrams:
            if tgram in self.index:
                for doc_id in self.index[tgram]:
                    scores[doc_id] += 1

        score = []
        for doc_id, doc_score in scores.items():
            percent_score = doc_score / len(query_ngrams)
            score.append({"id": doc_id, "score": percent_score})

        return sorted(score, key=lambda item: item["score"], reverse=True)


def query_counts(result: list[dict], threshold: int = 50) -> list[dict]:
    filtered_items = []
    max_score = 0.0

    for item in result:
        score = int((item["score"]) * 100)
        if score > max_score:
            max_score = float(score)
        if score >= threshold:
            filtered_items.append({"id": item["id"], "score": score})
    return {
        "items": filtered_items,
        "count": len(filtered_items),
        "max_score": max_score,
    }


def print_search_report(query: str, search_report: dict, documents: dict):
    print(f"Result for query: '{query}'")
    print("-" * 50)

    if not search_report["items"]:
        print("Nothing found")
        return

    for i, item in enumerate(search_report["items"], start=1):
        doc_id = item["id"]
        score = item["score"]
        title = documents[doc_id]["title"]
        print(f"{i}. [ID: {doc_id}] {title:<30} -> ({score:.2f}%)")
