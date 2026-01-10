from rdbms.database import Database

db = Database()
print("Simple RDBMS REPL (type 'exit' to quit)")

while True:
    cmd = input("> ").strip()
    if cmd.lower() == "exit":
        break
    try:
        if cmd.startswith("CREATE TABLE"):
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
        elif cmd.startswith("INSERT"):
            name = cmd.split()[2]
            values = cmd[cmd.find("(")+1:cmd.find(")")].split(",")
            values = [v.strip().strip("'") for v in values]
            db.get_table(name).insert(values)
            print("Row inserted")
        elif cmd.startswith("SELECT"):
            name = cmd.split()[3]
            print(db.get_table(name).select())
        else:
            print("Unsupported command")
    except Exception as e:
        print("Error:", e)
