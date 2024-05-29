import logging
import re
import sqlite3
from typing import Optional, Union, Literal

import pandas
from pydash import py_

__doc__ = """
Interface to an SQLite3 database for storage, with accessor methods to both ingest
and generate Pandas dataframes or JSON dict lists 
"""

logger = logging.getLogger(__name__)

OptionalValueDict = Optional[dict[str, Union[int, float, str]]]

sql_type_from_json_type = {
    "string": "TEXT",
    "number": "NUMERIC",
    "integer": "INTEGER",
    "boolean": "INTEGER",
}

json_type_from_sql_type = {
    "TEXT": "string",
    "NUMERIC": "number",
    "INTEGER": "integer",
}

var_name_regex = re.compile(r"[^\W0-9]\w*")


def check_key_characters(key) -> bool:
    result = bool(var_name_regex.fullmatch(key))
    if not result:
        print(f"Error: skipping {key} as it is not a good variable name")
    return result


class SqliteAdaptor:
    def __init__(self, db_fname: str):
        self.db_fname = db_fname
        self.conn = self.make_conn()
        self.cursor = self.conn.cursor()

    def make_conn(self):
        return sqlite3.connect(self.db_fname)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def execute(self, *args):
        return self.cursor.execute(*args)

    def read_tables(self):
        rows = self.execute("SELECT name FROM sqlite_master").fetchall()
        return [r[0] for r in rows]

    def read_table_schema(self, table: str) -> dict:
        """
        Reads the table schema as a json schema of an object. AdditionalProperties
        are set to False so that json-schema can be used to validate incoming dict.

        :param schema: dict - e.g. {
            "type": "object",
            "properties": {
                "row_id": {"type": "integer"},
                "description": {"type": "string"},
                "amount": {"type": "number"},
                "category": {"type": "string"},
            },
            "additionalProperties": False,
        }
        """
        queries = self.execute(f"PRAGMA table_info('{table}')").fetchall()
        props = {}
        for query in queries:
            name = query[1]
            data_type = json_type_from_sql_type[query[2]]
            props[name] = {"type": data_type}
        return {"type": "object", "properties": props, "additionalProperties": False}

    def create_table(self, table: str, schema: dict):
        """
        Creates table with json schema of an object representing table keys.
        Required properties are interpreted as primary keys.

        :param schema: dict - e.g. {
            "type": "object",
            "properties": {
                "row_id": {"type": "integer"},
                "description": {"type": "string"},
                "amount": {"type": "number"},
                "category": {"type": "string"},
            },
            "required": ["row_id"],
        }
        """
        columns = []
        for col, props in schema["properties"].items():
            if check_key_characters(col):
                sql_type = sql_type_from_json_type[props["type"].lower()]
                s = f"  {col} {sql_type} "
                if col in schema.get("required", []):
                    s += " PRIMARY KEY"
                columns.append(s)
        columns_sql = ",".join(columns)
        self.execute(f"CREATE TABLE IF NOT EXISTS {table} (\n{columns_sql}\n)\n")
        self.commit()

    def add_columns(self, table: str, schema: dict):
        """
        Adds columns described in a schema to a table.

        :param schema: dict - e.g.
        {
            type: "object",
            "properties": {
                "column_text_a": { "type": "string" }
                "column_float_b": { "type": "number" }
            }
        }
        """
        for name, props in schema["properties"].items():
            if check_key_characters(name):
                sqlite_type = sql_type_from_json_type[props["type"].lower()]
                self.execute(f"ALTER TABLE {table} ADD '{name}' '{sqlite_type}'")
        self.commit()

    def drop_table(self, table: str):
        if table in self.read_tables():
            self.execute(f"DROP TABLE {table}")
            self.commit()

    def rename_table(self, table: str, new_table: str):
        if table in self.read_tables():
            new_table = py_.snake_case(new_table)
            self.execute(f"ALTER TABLE {table} RENAME to {new_table}")
            self.commit()

    def execute_to_df(self, sql: str, params=None):
        return pandas.read_sql_query(sql, self.conn, params=params)

    def set_from_df(
            self, table: str, df: pandas.DataFrame, index=False,
            if_exists: Literal["fail", "append", "replace"] = "append"
    ):
        """
        :param df: pandas.Dataframe
        """
        df.to_sql(con=self.conn, name=table, index=index, if_exists=if_exists)
        self.commit()

    def replace_with_df(self, table: str, df: pandas.DataFrame, index=False):
        self.set_from_df(table, df, index=index, if_exists="replace")

    def build_condition_sql_and_params(
            self, value_by_key: OptionalValueDict, head="WHERE", separator=" AND "
    ):
        sql = ""
        params = []
        if value_by_key:
            lines = []
            for k, v in value_by_key.items():
                if check_key_characters(k):
                    lines.append(f"{k} = ? ")
                    params.append(str(v))
            if len(lines):
                column_str = separator.join(lines)
                sql += f"{head} {column_str} "
        return sql, params

    def build_select_sql_and_params(self, table: str, where: OptionalValueDict):
        where_sql, where_params = self.build_condition_sql_and_params(where)
        return f"SELECT * FROM {table} " + where_sql, where_params

    def read_rows(self, table: str, where: OptionalValueDict = None) -> [tuple]:
        sql, params = self.build_select_sql_and_params(table, where)
        return list(self.execute(sql, params))

    def read_one_row(self, table: str, where: OptionalValueDict = None) -> tuple:
        sql, params = self.build_select_sql_and_params(table, where)
        return self.execute(sql, params).fetchone()

    def read_df(self, table: str, where: OptionalValueDict = None) -> pandas.DataFrame:
        sql, params = self.build_select_sql_and_params(table, where)
        return pandas.read_sql_query(sql, self.conn, params=params)

    def read_dicts(self, table: str, where: OptionalValueDict = None) -> [dict]:
        return self.read_df(table, where).to_dict(orient="records")

    def read_one_dict(self, table: str, where: OptionalValueDict = None) -> dict:
        sql, params = self.build_select_sql_and_params(table, where)
        df = pandas.read_sql_query(sql + " LIMIT 1", self.conn, params=params)
        entries = df.to_dict(orient="records")
        if len(entries):
            return entries[0]
        else:
            return {}

    def read_csv(self, table: str) -> str:
        return self.read_df(table).to_csv(index=False)

    def insert(self, table: str, vals):
        """
        :param vals:
            <k>: <v>
        """
        params = []
        questions = []
        keys = []
        for key, val in vals.items():
            if check_key_characters(key):
                keys.append(key)
                questions.append("?")
                params.append(val)
        if len(keys):
            key_str = ",".join(keys)
            queston_str = ",".join(questions)
            self.execute(
                f"INSERT INTO {table} ({key_str}) VALUES ({queston_str})", params
            )
            self.commit()
            return self.cursor.lastrowid
        return None

    def update(self, table: str, where: OptionalValueDict, vals: OptionalValueDict):
        """
        :param vals:
            <k>: <v>
        """
        sql = f"UPDATE {table} "
        params = []
        if vals:
            set_sql, set_params = self.build_condition_sql_and_params(
                vals, separator=", ", head="SET"
            )
            params.extend(set_params)
            sql += set_sql + " "
        if where:
            where_sql, where_params = self.build_condition_sql_and_params(where)
            params.extend(where_params)
            sql += where_sql
        self.execute(sql, params)
        self.commit()

    def delete(self, table: str, where: OptionalValueDict):
        """
        :param vals:
            <k>: <v>
        """
        where_sql, params = self.build_condition_sql_and_params(where)
        self.execute(f"DELETE FROM {table} " + where_sql, params)
        self.commit()
