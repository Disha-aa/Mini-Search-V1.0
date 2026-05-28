from storage import DOCUMENTS, log_query
from engine import build_index, search



def output(query: str, result: list[dict], documents: dict) -> tuple[int, float]:
    print(f"Result for query: '{query}'")
    print("-"*50)
    results_count = 0
    max_score = 0.0

    for i, item in enumerate(result, start=1):
        doc_id = item['id']
        score = int(item['score'] * 100)
        if score > max_score:
            max_score = score

        if score >= 50:
            title = documents[doc_id]['title']
            print(f"{i}. [ID: {doc_id}] {title:<30} -> ({score:.2f}%)")
            results_count += 1
    return results_count, max_score

def main():
    documents = dict(DOCUMENTS)
    data_index = build_index(documents)
    while True:
        user_input = input("Enter a query (or '0' to stop): ")
        if user_input == "0":
            return

        if not user_input.strip():
            print("Error: empty input")
            continue
        
        search_result = search(user_input, data_index)
        output(user_input, search_result, documents)

        filename = "log_report"
        results_count, max_score = output(user_input, search_result, documents)
        log_query(filename, user_input, results_count, max_score)

if __name__ == "__main__":
    main()
