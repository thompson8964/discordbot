import toml
import mysql.connector

from datetime import datetime
now = datetime.now()

with open('config.toml', 'r') as f:
    data = toml.load(f)
serverkey = data["serverkey"]

passw = data["dbpsword"]


if __name__ == "__main__":
    # To connect MySQL database
    db = mysql.connector.connect(
        host=data["host"],
        user='admin',
        password=passw,
        db='chatbot',
    )

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT * FROM user_data WHERE user_payment_info=1;")

  #  myresult = cursor.fetchall()



    #query = "SELECT * FROM user_data WHERE user_payment_info = 2;"

    #cursor.execute(query)
    rows = cursor.fetchall()

    print(rows)
    #close the connection
    db.close()


