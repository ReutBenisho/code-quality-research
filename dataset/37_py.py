import sys
import mysql.connector

def main():
    if len(sys.argv) - 1 < 1:
        print("You should give an entry parameter...")
        print("Usage: ./sql <parameter>")
        return 0

    con = mysql.connector.connect(host="kikoo", user="user", password="userpass")
    query = con.cursor()
    sql = "SELECT * FROM test WHERE Value = '" + sys.argv[1] + "'"
    query.execute(sql)
    res = query.fetchall()

    print("Results: ")
    if res:
        for row in res:
            print("\t" + str(row[0]))

    return 0

if __name__ == "__main__":
    main()