export const VULNERABLE_SAMPLE = `import os
import sqlite3
password = "admin123"
user_id = input("Enter ID: ")
query = "SELECT * FROM users WHERE id = " + user_id
os.system("cat /var/log/app/" + user_id + ".log")

conn = sqlite3.connect("app.db")
rows = conn.execute(query).fetchall()

for row in rows:
    print(row)
`;


export const EMPTY_SAMPLE = `def main():
    pass


if __name__ == "__main__":
    main()
`;
