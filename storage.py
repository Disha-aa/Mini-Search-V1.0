from datetime import datetime
from types import MappingProxyType as mpt

_documents: dict[int, dict[str, str]] = {
    1: {
        "title": "Python Backend Development",
        "content": "Learn how to build scalable backends using Python."
    },
    2: {
        "title": "FastAPI REST API Guide",
        "content": "FastAPI is a modern, fast web framework for building APIs."
    },
    3: {
        "title": "PostgreSQL Optimization Techniques",
        "content": "Deep dive into indexes, query planning, and database tuning."
    },
    4: {
        "title": "Docker Containers for Beginners",
        "content": "How to isolate your applications and deploy them anywhere easily."
    },
    5: {
        "title": "Asynchronous Programming in Python",
        "content": "Master async and await keywords to build high-performance services."
    },
    6: {
        "title": "Git Version Control Best Practices",
        "content": "Learn rebasing, merging, and managing clean commit history in Git."
    },
    7: {
        "title": "Introduction to Go Language",
        "content": "Why backend developers switch from Python to Go for high load concurrency."
    },
    8: {
        "title": "Redis as a Caching Layer",
        "content": "Speed up your FastAPI application by caching heavy database queries."
    },
    9: {
        "title": "Apache Kafka Event Streaming",
        "content": "Building event-driven microservices architecture using Kafka brokers."
    },
    10: {
        "title": "REST API Authentication Methods",
        "content": "Implementing JWT tokens and OAuth2 safely in modern web apps."
    }
}

DOCUMENTS = mpt(_documents)

def log_query(filename: str, query: str, results_count: int, max_score: float) -> None:
    try:
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{log_time}] Query: '{query}' -> Found: {results_count} docs, Best score: {max_score:.1f}%"

        with open(filename, mode="a", encoding='utf-8') as file:
            file.write(f"{log_line}\n")
    except IOError as e:
        print(f"[ERROR] The file could not be saved: {e}")