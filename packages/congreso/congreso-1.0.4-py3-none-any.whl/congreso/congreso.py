import requests, gzip
r = requests.get('https://zenodo.org/api/records/11195944')
zenodo_metadata = r.json()


import urllib.request
import json
import pandas as pd
from collections import Counter
from datetime import datetime



def load_jsons(roman_numerals: list[str]):
  """Loads multiple JSON files from Zenodo.

  This function takes a list of Roman numerals (`roman_numerals`) as input, representing the terms to be analyzed.
  It retrieves the metadata of the corresponding JSON files from Zenodo and downloads them.

  Args:
      roman_numerals (list): A list of Roman numerals representing the terms to be analyzed (e.g., ["XI", "XII"]).

  Returns:
      None: This function modifies global variables to store the loaded JSON data. Each term is stored as a separate variable with the corresponding Roman numeral as its name (e.g., XI, XII).
  """
  dict_ = {}
  file_dict = {d['key']:d['links']['self'] for d in zenodo_metadata["files"]}
  for numeral in roman_numerals:
      filename = f'{numeral}.json.gz'
      urllib.request.urlretrieve(file_dict[filename],filename)
      with gzip.open(filename, 'rt', encoding='UTF-8') as f:
          dict_[numeral] = json.load(f)
  return dict_



def get_all_fields(term: list[dict]):
  """Gets all unique fields (keys) present in a list of documents.

  This function takes a list of documents (`term`) as input and returns a list containing all the unique field names (keys) found in those documents.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      list: A list containing all the unique field names (keys) present in the documents.
  """
  all_fields = set()
  for doc in term:
    all_fields.update(doc.keys())
  return list(all_fields)



def num_docs_term(term: list[dict]):
  """Counts the number of documents in a list.

  This function takes a list of documents (`term`) as input and returns the total number of documents in the list.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      int: The number of documents in the list.
  """
  document_count = len(term)
  return document_count



def get_docs_by_date(term: list[dict], date: str):
  """Filters documents by a specific date.

  This function takes a list of documents (`term`) and a date string (`date`) as input. It iterates through the documents and returns a list containing only the documents that have a matching "fecha" field (date) after removing leading/trailing spaces.

  Args:
      term (list): A list of dictionaries representing documents.
      date (str): The date string to filter by (YYYYMMDD format).

  Returns:
      list: A list containing documents that have the matching "fecha" field (date).
            If no documents match the date, it prints a message indicating no documents were found and returns an empty list.
  """
  docs_list = []
  for doc in term:
    if doc["fecha"].strip() == date:
      docs_list.append(doc)
  if not docs_list:
      term_name = term[0]["legislatura"]
      print(f"No documents on {date} for the term {term_name}")
  return docs_list



def get_documents_interval_dates(term: list[dict], start_date: str, end_date: str):
  """Filters documents by a date interval.

  This function takes a list of documents (`term`), a start date string (`start_date`), and an end date string (`end_date`) as input. It iterates through the documents and returns a list containing only the documents that have a matching "fecha" field (date) within the specified interval after removing leading/trailing spaces from dates.

  Args:
      term (list): A list of dictionaries representing documents.
      start_date (str): The start date string of the interval (YYYYMMDD format).
      end_date (str): The end date string of the interval (YYYYMMDD format).

  Returns:
      list: A list containing documents that have the matching "fecha" field (date) within the interval.
            If no documents match the date interval, it prints a message indicating no documents were found and returns an empty list.
  """
  docs_list = []
  start_date = datetime.strptime(start_date, "%Y%m%d").date()
  end_date = datetime.strptime(end_date, "%Y%m%d").date()
  for doc in term:
    doc_date = datetime.strptime(doc["fecha"].strip(), "%Y%m%d").date()
    if start_date <= doc_date <= end_date:
      docs_list.append(doc)
  if not docs_list:
      term_name = term[0]["legislatura"]
      print(f"No documents between {start_date} and {end_date} for the term {term_name}")
  return docs_list



def key_word_search(word: str, term: list[dict]):
  """Filters documents containing a specific keyword.

  This function takes a keyword string (`word`) and a list of documents (`term`) as input. It iterates through the documents and returns a list containing only the documents that have the keyword string present within their "texto" field (text).

  Args:
      word (str): The keyword to search for.
      term (list): A list of dictionaries representing documents.

  Returns:
      list: A list containing documents that have the keyword string within their "texto" field.
            If no documents contain the keyword, it prints a message indicating no documents were found and returns an empty list.
  """
  docs_list = []
  for doc in term:
    if word in doc["texto"]:
      docs_list.append(doc)
  if not docs_list:
      term_name = term[0]["legislatura"]
      print(f"No documents containing '{word}' for the term {term_name}")
  return docs_list



def count_docs_with_aperance(word: str, term: list[dict]):
  """
  Counts the number of documents in a list where a specific word appears in the "texto" field.

  Args:
      word (str): The word to search for.
      term (list): A list of dictionaries representing documents.

  Returns:
      int: The number of documents containing the word.
  """
  count = 0
  for doc in term:
    if word in doc["texto"]:
      count+= 1
  return count



def mentions_per_doc(word: str, term: list[dict]):
  """
  Calculates the number of times a phrase (sequence of words) appears in each document of a list.

  Args:
      word (str): The phrase (sequence of words) to search for.
      term (list): A list of dictionaries representing documents.

  Returns:
      list: A list containing the number of times the phrase appears in each document.
  """
  count = [0]*len(term)
  word_list = word.split()
  word_len = len(word_list)
  for i, doc in enumerate(term):
      words = doc["texto"].split()
      for j in range(len(words) - word_len + 1):
          if words[j:j+word_len] == word_list:
              count[i] += 1
  return count



def display_field_values(term: list[dict], field: str):
  """
  Analyzes the values of a specific field in a list of documents and displays a DataFrame showing the unique values and their corresponding number of documents.

  Args:
      term (list): A list of dictionaries representing documents.
      field (str): The name of the field to analyze.

  Returns:
      pandas.DataFrame: A DataFrame with two columns:
          - field: The unique values from the specified field.
          - 'Number of Documents': The number of documents containing each unique value.
  """
  field_values = [doc[field] for doc in term]
  counts = Counter(field_values)
  df = pd.DataFrame(list(counts.items()), columns=[field, 'Number of Documents'])
  df = df.sort_values('Number of Documents', ascending=False)
  df = df.reset_index(drop=True)
  return df



def filter_field_by_value(term: list[dict], field: str, value: str):
  """
  Filters documents in a list based on a specific field and value.

  This function takes a list of documents (`term`), a field name (`field`), and a value (`value`) as input. It iterates through the documents and returns a new list containing only the documents where the specified field (`field`) has the exact matching value.

  Args:
      term (list): A list of dictionaries representing documents.
      field (str): The name of the field to filter by.
      value: The value to filter for.

  Returns:
      list: A list containing documents where the specified field (`field`) has the exact matching value.
  """
  filtered_docs = []
  for doc in term:
    if doc[field] == value:
      filtered_docs.append(doc)
  return filtered_docs



def visualize_ndia(term: list[dict]):
  """
  Analyzes the 'ndia' field of documents in a list (assuming it represents days) and creates visualizations for the number of documents per day.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      tuple: A tuple containing two lists:
          - days: A list of days (integers).
          - counts: A list of document counts for each day.
  """
  days = [int(doc["ndia"]) for doc in term if "ndia" in doc]
  day_counts = Counter(days)
  sorted_days_counts = sorted(day_counts.items(), key=lambda x: x[0])
  days, counts = zip(*sorted_days_counts)
  days = days[::-1]
  counts = counts[::-1]
  return days, counts



def productive_days_percentage(term: list[dict]):
  """
  Calculates the percentage of days with documents and the total number of documents, considering the 'ndia' and 'fecha' fields. Basically thr amound of days with some production on the whole term.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      tuple: A tuple containing two values:
          - percentage (float): The percentage of days with documents (None if 'ndia' is empty).
          - num_docs (int): The total number of documents (None if 'ndia' is empty).
  """
  ndias = [0]*len(term)
  fechas = [0]*len(term)
  for i, doc in enumerate(term):
    ndias[i] = int(doc["ndia"])
    fechas[i] = datetime.strptime(doc["fecha"].strip(), "%Y%m%d")
  if not ndias:
      return None, None
  max_ndia = max(ndias)
  first_fecha = min(fechas)
  last_fecha = max(fechas)
  total_days = (last_fecha - first_fecha).days + 1
  percentage = (max_ndia / total_days) * 100
  return percentage, len(ndias)



def docs_per_day(term: list[dict]):
  """
  Calculates thethe documents produced per day on average for a concreet term.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      tuple: A tuple containing two values:
          - average (float): The average of documents per day.
          - num_docs (int): The total number of documents.
  """
  fechas = [0]*len(term)
  for i, doc in enumerate(term):
    fechas[i] = datetime.strptime(doc["fecha"].strip(), "%Y%m%d")
  first_fecha = min(fechas)
  last_fecha = max(fechas)
  total_days = (last_fecha - first_fecha).days + 1
  num_docs = num_docs_term(term)
  average = (num_docs / total_days)
  return average, num_docs



def filter_encabezado(term: list[dict]):
  """
  Filters documents in a list based on the value of the "encabezado" field. Tis is usefull since there are only 2 types of encabezado, BOGC and DS.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      tuple: A tuple containing three lists:
          - BOCG: A list of documents with "encabezado" equal to "BOCG".
          - DS: A list of documents with "encabezado" equal to "DS".
          - others: A list of documents with "encabezado" not equal to "BOCG" or "DS".
  """
  BOCG = []
  DS = []
  others = []
  for doc in term:
    if doc["encabezado"].strip() == "BOCG":
      BOCG.append(doc)
    elif doc["encabezado"].strip() == "DS":
      DS.append(doc)
    else:
      others.append(doc)
  return BOCG, DS, others



def add_texto_length(term: list[dict]):
  """
  Adds a new key 'texto_length' to each document in a list, containing the length of the text in the 'texto' field.

  Args:
      term (list): A list of dictionaries representing documents.

  Returns:
      list: A new list of dictionaries with the added 'texto_length' key field.
  """
  new_term = []
  for doc in term:
      new_doc = doc.copy()
      new_doc['texto_length'] = len(doc['texto'])
      new_term.append(new_doc)
  return new_term



def docs_filtered_by_lenght(term: list[dict], upper_threshold = 1000000, lower_threshold = 0):
  """
  Filters documents in a list based on the length of the text in the 'texto' field.

  Args:
      term (list): A list of dictionaries representing documents.
      upper_threshold (int, optional): The upper limit for the text length (inclusive). Defaults to 1000000.
      lower_threshold (int, optional): The lower limit for the text length (inclusive). Defaults to 0.

  Returns:
      tuple: A tuple containing two values:
          - threshold_docs: A list of documents within the specified text length range.
          - count: The number of documents within the specified text length range.
  """
  threshold_docs = []
  count = 0
  for doc in term:
    if lower_threshold <= doc["texto_length"] <= upper_threshold:
       threshold_docs.append(doc)
       count += 1
  return threshold_docs, count