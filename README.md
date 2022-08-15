# nl2sql

## Data

The Cohere-formatted data is available in `data/` with the following versions:
```
* {train/validation/test}.txt: full datasets
* {train/validation/test}.nexs{100/1000}.txt: datasets truncated to the first {100/1000} examples
```

The (current) formatting for each example is as follow: `{table_name} <c> {col_name1} <t> {col_type1} ... <c> {col_name_N} <t> {col_type_N}  <i> {natural language question} <s> {SQL query}`
If there is no table name provided, we use the dataset ID.
