from engine import InvertedIndex, print_search_report, query_counts
from security import rate_limit, require_role
from storage import DOCUMENTS, log_query


@require_role(required_role="user")
@rate_limit(max_calls=2, period_seconds=10)
def handle_search_request(user_input, index_instance, DOCUMENTS):
    documents = dict(DOCUMENTS)

    search_result = index_instance.search(user_input)
    counts_result = query_counts(search_result, threshold=50)

    print_search_report(user_input, counts_result, documents)

    filename = "log_report"
    log_query(filename, user_input, counts_result)


def main():
    documents = dict(DOCUMENTS)
    index_instance = InvertedIndex()
    index_instance.build_index(documents)

    current_user = {"username": "Disha", "role": "user"}

    while True:
        user_input = input("Enter a query (or '0' to stop): ")
        if user_input == "0":
            return

        if not user_input.strip():
            print("Error: empty input")
            continue

        try:
            handle_search_request(
                user_input, index_instance, documents, user=current_user
            )
        except PermissionError as e:
            print(f"[ACCESS DENIED] {e}")
        except ValueError as e:
            print(f"[RATE LIMIT] {e}")


if __name__ == "__main__":
    main()
