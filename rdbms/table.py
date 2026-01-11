# rdbms/table.py

class Table:
    def __init__(self, name, columns, column_types=None, primary_key=None, unique_keys=None):
        self.name = name
        self.columns = columns
        self.column_types = column_types or [str] * len(columns)
        self.primary_key = primary_key
        self.unique_keys = unique_keys or []
        self.rows = []
        self.indexes = {}

        # Build indexes for primary and unique keys
        for key in self.unique_keys + ([primary_key] if primary_key else []):
            self.indexes[key] = {}

    def cast_values(self, values):
        """Cast values to column types"""
        return [typ(v) for typ, v in zip(self.column_types, values)]

    def insert(self, values):
        values = self.cast_values(values)
        row = dict(zip(self.columns, values))
        # Check unique constraints
        for key, index in self.indexes.items():
            if row[key] in index:
                raise ValueError(f"Duplicate value for {key}")
        self.rows.append(row)
        row_id = len(self.rows) - 1
        for key, index in self.indexes.items():
            index[row[key]] = row_id

    def select(self, where=None):
        if not where:
            return self.rows
        col, val = where
        col_index = self.columns.index(col)
        val = self.column_types[col_index](val)  # cast WHERE value to column type
        if col in self.indexes:
            idx = self.indexes[col].get(val)
            return [self.rows[idx]] if idx is not None else []
        return [r for r in self.rows if r[col] == val]

    def update(self, where, updates):
        count = 0
        for row in self.select(where):
            for k, v in updates.items():
                col_index = self.columns.index(k)
                row[k] = self.column_types[col_index](v)  # cast update value
            count += 1
        return count

    def delete(self, where):
        col, val = where
        col_index = self.columns.index(col)
        val = self.column_types[col_index](val)
        before = len(self.rows)
        self.rows = [r for r in self.rows if r[col] != val]
        return before - len(self.rows)
