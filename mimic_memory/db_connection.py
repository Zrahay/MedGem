"""
db_connection.py

Handles database connection to MIMIC-IV.
Supports PostgreSQL or DuckDB depending on configuration.
"""

import yaml
import duckdb
import psycopg2
from psycopg2.extras import RealDictCursor


class MIMICDatabase:
    def __init__(self, config_path="config/db_config.yaml"):
        self.config = self._load_config(config_path)
        self.db_type = self.config["database"]["type"]

        if self.db_type == "duckdb":
            self.conn = duckdb.connect(self.config["database"]["path"])
        elif self.db_type == "postgres":
            self.conn = psycopg2.connect(
                dbname=self.config["database"]["dbname"],
                user=self.config["database"]["user"],
                password=self.config["database"]["password"],
                host=self.config["database"]["host"],
                port=self.config["database"]["port"],
                cursor_factory=RealDictCursor
            )
        else:
            raise ValueError("Unsupported database type")

    def _load_config(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def query(self, sql, params=None):
        """
        Executes a SQL query safely and returns results.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, params or ())
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            return {"error": str(e)}
