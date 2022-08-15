# nl2sql

## Data

The Cohere-formatted version of [WikiSQL](https://huggingface.co/datasets/wikisql) ([paper here](https://arxiv.org/abs/1709.00103)) and [Spider](https://github.com/taoyds/spider) is available in `data/` with the following versions:
```
* {train/validation/test}.txt: full datasets
* {train/validation/test}.nexs{100/1000}.txt: datasets truncated to the first {100/1000} examples
```
The data in `data/wikisql` uses the tables and SQL queries from WikiSQL largely as-is. The data in `data/bigquery` removes whitespace and punctuation from the schema and quotes strings in SQL queries to be compatible with BigQuery.

The (current) formatting for each example is as follow: `{table_name} <c> {col_name1} <t> {col_type1} ... <c> {col_name_N} <t> {col_type_N}  <i> {natural language question} <s> {SQL query}`.
If there is no table name provided, we use the dataset ID.

The set of unique original tables (with rows) are available in `data/all_tables.jsonl` with no other processing.

The Spider data is formatted similarly to the WikiSQL data, with the major exception that examples in Spider contain multiple tables (a database). We format the tables using `</t>` as a delimiter. Also, there is no test set in Spider, as users are expected to submit to the test server to evaluate on the test split. The table schema are available in `data/spider/tables.json` (copied from the original data release) and the full tables need to be downloaded from the original release [here](https://yale-lily.github.io/spider).
