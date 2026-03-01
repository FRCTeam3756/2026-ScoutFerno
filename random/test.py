import sqlite3 as sql3

connection = sql3.connect("test.db")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS people")

cursor.execute("""
CREATE TABLE IF NOT EXISTS people (
    name TEXT PRIMARY KEY NOT NULL,
    age INTEGER, 
    height_cm INTEGER
)
""")

people = [
    ("Gabe", 10, 185),
    ("Ethan", 12, 175),
]

cursor.executemany(
    "INSERT INTO people (name, age, height_cm) VALUES (?, ?, ?)",
    people
)

connection.commit()

cursor.execute("SELECT * FROM people")

rows = cursor.fetchall()

for i, row in enumerate(rows):
    print(i)

connection.close()