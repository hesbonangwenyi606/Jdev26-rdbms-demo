class Table:
    def __init__(self, name, columns, primary_key=None, unique_keys=None):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.unique_keys = unique_keys or []
        self.rows = []
        self.indexes = {}

        for key in self.unique_keys + ([primary_key] if primary_key else []):
            self.indexes[key] = {}

    def insert(self, values):
        row = dict(zip(self.columns, values))
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
        if col in self.indexes:
            idx = self.indexes[col].get(val)
            return [self.rows[idx]] if idx is not None else []
        return [r for r in self.rows if r[col] == val]

    def update(self, where, updates):
        for row in self.select(where):
            for k, v in updates.items():
                row[k] = v

    def delete(self, where):
        col, val = where
        self.rows = [r for r in self.rows if r[col] != val]
