# nl2sql

## Data

The Cohere-formatted version of [WikiSQL](https://huggingface.co/datasets/wikisql) ([paper here](https://arxiv.org/abs/1709.00103)) and [Spider](https://github.com/taoyds/spider) are available in `data/` with the following versions:
```
* {train/validation/test}.txt: full datasets
* {train/validation/test}.nexs{100/1000}.txt: datasets truncated to the first {100/1000} examples
```
The data in `data/wikisql/wikisql` uses the tables and SQL queries from WikiSQL largely as-is. The data in `data/bigquery` removes whitespace and punctuation from the schema and quotes strings in SQL queries to be compatible with BigQuery.

The (current) formatting for each example is as follow: `{table_name} <c> {col_name1} <t> {col_type1} ... <c> {col_name_N} <t> {col_type_N}  <i> {natural language question} <s> {SQL query}`.
If there is no table name provided, we use the dataset ID.

The set of unique original WikiSQL tables (with rows) is available in `data/wikisql/all_tables.jsonl` with no other processing.

The Spider data is formatted similarly to the WikiSQL data, with the major exception that examples in Spider contain multiple tables (a database). We format the tables using `</t>` as a delimiter. Also, there is no test set in Spider, as users are expected to submit to the test server to evaluate on the test split. The table schema are available in `data/spider/tables.json` (copied from the original data release) and the full tables need to be downloaded from the original release [here](https://yale-lily.github.io/spider).

Files with `augN` in the name have had data augmentation applied to them (increasing the size of the data by a factor of N, an integer). We expand data by shuffling the order of columns when and linearizing the table, as well as shuffling the order of tables for Spider. Code for further data expansion are available in `data_processing.ipynb`.

## Evaluation

A notebook for evaluating ngram overlap is available in `evaluation.ipynb`.
