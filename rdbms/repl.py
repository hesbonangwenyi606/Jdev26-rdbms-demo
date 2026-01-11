# rdbms/repl.py

from rdbms.database import Database

db = Database()
print("Simple RDBMS REPL (type 'exit' to quit)")

def print_rows(rows):
    if not rows:
        print("No rows found")
        return
    print(" | ".join(rows[0].keys()))
    for r in rows:
        print(" | ".join(str(v) for v in r.values()))

while True:
    cmd = input("> ").strip()
    if cmd.lower() == "exit":
        break
    try:
        cmd_upper = cmd.upper()

        # --- CREATE TABLE ---
        if cmd_upper.startswith("CREATE TABLE"):
            # Example: CREATE TABLE users (id INT PRIMARY, name TEXT);
            name = cmd.split()[2]
            cols_raw = cmd[cmd.find("(")+1:cmd.find(")")].split(",")
            columns, types, pk, uniq = [], [], None, []
            for c in cols_raw:
                parts = c.strip().split()
                col_name = parts[0]
                col_type = parts[1].upper() if len(parts) > 1 else "TEXT"
                columns.append(col_name)
                types.append(int if col_type == "INT" else str)
                if "PRIMARY" in parts:
                    pk = col_name
                if "UNIQUE" in parts:
                    uniq.append(col_name)
            db.create_table(name, columns, types, pk, uniq)
            print("Table created")

        # --- INSERT ---
        elif cmd_upper.startswith("INSERT"):
            # Example: INSERT INTO users VALUES (1, 'Alice');
            name = cmd.split()[2]
            values = cmd[cmd.find("(")+1:cmd.find(")")].split(",")
            values = [v.strip().strip("'") for v in values]
            db.get_table(name).insert(values)
            print("Row inserted")

        # --- SELECT ---
        elif cmd_upper.startswith("SELECT"):
            # Example: SELECT * FROM users;
            name = cmd.split()[3].rstrip(";")
            rows = db.get_table(name).select()
            print_rows(rows)

        # --- UPDATE ---
        elif cmd_upper.startswith("UPDATE"):
            # Example: UPDATE users SET name='Charlie' WHERE id=1;
            parts = cmd.split("SET")
            table_name = parts[0].split()[1].strip()
            set_part = parts[1].split("WHERE")[0].strip()
            where_part = parts[1].split("WHERE")[1].strip().rstrip(";")

            set_col, set_val = set_part.split("=")
            set_col = set_col.strip()
            set_val = set_val.strip().strip("'")

            where_col, where_val = where_part.split("=")
            where_col = where_col.strip()
            where_val = where_val.strip().strip("'")

            table = db.get_table(table_name)
            count = table.update((where_col, where_val), {set_col: set_val})
            print(f"{count} row(s) updated")

        # --- DELETE ---
        elif cmd_upper.startswith("DELETE"):
            # Example: DELETE FROM users WHERE id=2;
            parts = cmd.split("WHERE")
            table_name = parts[0].split()[2].strip()
            where_part = parts[1].strip().rstrip(";")

            where_col, where_val = where_part.split("=")
            where_col = where_col.strip()
            where_val = where_val.strip().strip("'")

            table = db.get_table(table_name)
            count = table.delete((where_col, where_val))
            print(f"{count} row(s) deleted")

        else:
            print("Unsupported command")

    except Exception as e:
        print("Error:", e)
