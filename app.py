from engine import build_index, print_search_report, query_counts, search
from security import rate_limit, require_role
from storage import DOCUMENTS, log_query


@require_role(required_role="user")
@rate_limit(max_calls=2, period_seconds=10)
def handle_search_request(user_input, data_index, DOCUMENTS):
    documents = dict(DOCUMENTS)

    search_result = search(user_input, data_index)
    counts_result = query_counts(search_result, threshold=50)

    print_search_report(user_input, counts_result, documents)

    filename = "log_report"
    log_query(filename, user_input, counts_result)


def main():
    documents = dict(DOCUMENTS)
    data_index = build_index(documents)
    current_user = {"username": "Disha", "role": "user"}

    while True:
        user_input = input("Enter a query (or '0' to stop): ")
        if user_input == "0":
            return

        if not user_input.strip():
            print("Error: empty input")
            continue

        try:
            handle_search_request(user_input, data_index, documents, user=current_user)
        except PermissionError as e:
            print(f"[ACCESS DENIED] {e}")
        except ValueError as e:
            print(f"[RATE LIMIT] {e}")


if __name__ == "__main__":
    main()
