# rdbms/database.py

from rdbms.table import Table

class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns, column_types=None, primary_key=None, unique_keys=None):
        self.tables[name] = Table(name, columns, column_types, primary_key, unique_keys)

    def get_table(self, name):
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist")
        return self.tables[name]

    def join(self, t1, t2, k1, k2):
        result = []
        for r1 in t1.rows:
            for r2 in t2.rows:
                if r1[k1] == r2[k2]:
                    result.append({**r1, **r2})
        return result
