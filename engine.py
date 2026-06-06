import collections as col
import string


def normalize(text: str) -> str:
    clean_chars = [
        char.lower() if char not in string.punctuation else " " for char in text.strip()
    ]
    return "".join(clean_chars)


def build_ngrams(word: str, n: int = 3) -> set[str]:
    if len(word) < n:
        return {f"_{word}_"}
    word = f"_{word}_"
    return {word[i : i + n] for i in range(len(word) - n + 1)}


def build_index(documents: dict[int, dict], n: int = 3) -> dict[str, set[int]]:
    index = col.defaultdict(set)

    for doc_id, doc_data in documents.items():
        text = f"{doc_data['title']} {doc_data['content']}"
        words = normalize(text).split()
        for word in words:
            trigrams = build_ngrams(word, n)
            for trigram in trigrams:
                index[trigram].add(doc_id)

    return dict(index)


def search(query: str, index: dict[str, set[int]], n: int = 3) -> list[dict]:
    normal_query = normalize(query)
    if not normal_query.strip():
        return []
    query_ngrams = build_ngrams(normal_query, n)

    scores = col.defaultdict(int)
    for tgram in query_ngrams:
        if tgram in index:
            for doc_id in index[tgram]:
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
            max_score = score
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
