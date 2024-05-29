# sqladaptor

Transferring data, stored as JSON or Pandas, into an SQL database and back again.

## Why?

Building webserver protoytpes, you will often save your data as JSON or Pandas files.
At some point though, you will want to transition to a database where
updating/inserting data to disk is more efficient. 

SqlAdaptor allows an easy transition to such a database.
This includes methods to search using dicts, and
to return rows as dicts for web-servers. 

This is possible
because there is an equivalence between JSON dict lists, Pandas DataFrames
and SQL tables - they are all tabular arrangements of columnar data.

## Installation

```bash
pip install sqladaptor
```

## Basic Usage

```python
from sqladaptor.sqlite import SqliteAdaptor
import pandas

entries = [
    {"description": "this", "value": 1},
    {"description": "that", "value": 2}
]

db = SqliteAdaptor('db.sqlite')
db.set_from_df('data1', pandas.DataFrame(entries))

entries = db.read_dicts('data1')
# [
#   {'description': 'this', 'value': 1}, 
#   {'description': 'that', 'value': 2}
# ]

return_entries = db.read_dicts('data1', {"description": "this"})
# [{'description': 'this', 'value': 1}]

df = db.read_df("data1", {"value": 2})
#   description  value
# 0        that      2

db.update("data1", {"value": 2}, {"description": "altered"})
return_entries2 = db.read_dicts('data1', {"value": 2})
# [{'description': 'altered', 'value': 2}]
```

## The API

The key idea is to provide a JSON-like API for an SQL database. This will get provide
a simple way of moving JSON lists into a database. With the API, JSON lists are easily
returned. This is to simplify the transition of a good prototype into a production 
database.