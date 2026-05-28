# Key Features
· Fuzzy Search: The trigram algorithm allows you to find documents even if the user has misspelled a word.  
· Indexing: Automatic index creation from a dataset (documents).  
· Logging: Recording of all queries and their results in the log_report file for later analysis.  

## Project Architecture:
· app.py: entry point, processing of user input, and output of results.  
· engine.py: core engine containing the logic for text normalization, index building, and the search algorithm.  
· storage.py: data storage and query logging functionality.  

## Development history:
· The project was developed as a backend development exercise. 
· Currently, basic indexing and logging functionality has been implemented; integration with SQL databases is planned.