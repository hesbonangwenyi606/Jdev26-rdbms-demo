# rdbms/repl.py

from rdbms.database import Database

db = Database()
print("Simple RDBMS REPL (type 'exit' to quit)")

while True:
    cmd = input("> ").strip()
    if cmd.lower() == "exit":
        break
    try:
        # --- CREATE TABLE ---
        if cmd.upper().startswith("CREATE TABLE"):
            name = cmd.split()[2]
            cols = cmd[cmd.find("(")+1:cmd.find(")")].split(",")
            columns, pk, uniq = [], None, []
            for c in cols:
                parts = c.strip().split()
                columns.append(parts[0])
                if "PRIMARY" in parts:
                    pk = parts[0]
                if "UNIQUE" in parts:
                    uniq.append(parts[0])
            db.create_table(name, columns, pk, uniq)
            print("Table created")

        # --- INSERT ---
        elif cmd.upper().startswith("INSERT"):
            name = cmd.split()[2]
            values = cmd[cmd.find("(")+1:cmd.find(")")].split(",")
            values = [v.strip().strip("'") for v in values]
            db.get_table(name).insert(values)
            print("Row inserted")

        # --- SELECT ---
        elif cmd.upper().startswith("SELECT"):
            name = cmd.split()[3].rstrip(";")
            table = db.get_table(name)
            rows = table.select()
            if rows:
                # Print header
                print(" | ".join(rows[0].keys()))
                # Print rows
                for row in rows:
                    print(" | ".join(row.values()))
            else:
                print("No rows found")

        # --- UPDATE ---
        elif cmd.upper().startswith("UPDATE"):
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
        elif cmd.upper().startswith("DELETE"):
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

        # --- Unsupported command ---
        else:
            print("Unsupported command")

    except Exception as e:
        print("Error:", e)
