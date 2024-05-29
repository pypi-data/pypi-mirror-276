# Congreso Utils

## Description:
A Python package designed to streamline the analysis of legislative documents from the Congreso de los Diputados (Spain). This package is designed to help on the usage of the  data base https://doi.org/10.5281/zenodo.11195944 created by this authors. The data base contains 16 json files where each contains all the congres and senate records of the corresponding term. The terms are named after the term they represent (C, I, II, III,... XV). Whith this notebook you'll be able to:
- Load JSON data effortlessly from Zenodo
- Explore and filter documents using diverse criteria
- Analyze document content with text processing techniques
- Generate informative statistics and visualizations
- Term Selection and Data Loading:

## Loading Data: 
The first step is to load the JSON data using the load_jsons function, you will need to load the terms you are interested in. Pass a list containing the desired Roman numerals (terms) as input:

- from congreso import congreso as c (after installing this library)
- terms = ["XV", "XIV"]
- t = c.load_jsons(terms)

Use functions with term input:

fields = c.get_all_fields(t["XV"])
print(fields)

## Function Usage:

1. num_docs_term(term): Retrieves the number of documents for a specific term (e.g., num_docs_term(t["XV"])).
2. get_all_fields(term): Returns a list of all unique fields present in the documents for a term.
3. get_docs_by_date(term, date): Filters documents for a term based on a specific date (YYYYMMDD format).
4. get_documents_interval_dates(term, start_date, end_date): Filters documents for a term within a date range (YYYYMMDD format).
5. key_word_search(word, term): Finds documents for a term that contain a particular keyword within the "texto" field.
6. count_docs_with_aperance(word, term): Counts the number of documents for a term that contain a specified word within the "texto" field.
7. mentions_per_doc(word, term): Calculates the frequency of a phrase (sequence of words) within each document of a term's document list.
8. display_field_values(term, field): Analyzes the values of a particular field for a term, returning a DataFrame showing unique values and their corresponding document counts.
9. filter_field_by_value(term, field, value): Filters documents for a term based on a specific field and value.
10. visualize_ndia(term): (analyzes 'ndia' field for document counts per day)
11. productive_days_percentage(term): (calculates percentage of days with documents and total documents)
12. docs_per_day(term): (calculates average documents produced per day)
13. filter_encabezado(term: list[dict]) Filters documents based on a specific field ("encabezado" with only two types: "BOCG" and "DS"). Useful for focused searches.
14. add_texto_length(term: list[dict]) Adds a new field ("texto_length") to each document, containing the length of the text within the "texto" field. Facilitates text analysis based on length.
15. docs_filtered_by_lenght(term: list[dict], upper_threshold = 1000000, lower_threshold = 0) Filters documents based on the text length within the "texto" field. Useful for analyzing shorter or longer documents.

## License:
This package is distributed under the MIT License (see LICENSE file for details).

