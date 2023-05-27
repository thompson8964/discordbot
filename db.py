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
        db='discordBotDB',
    )

    cursor = db.cursor()

    cursor.execute("Show tables;")

    myresult = cursor.fetchall()

    print(myresult)

#insert

    data = {"timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
            "user_id": 1,
            "message_content": "a",
            "reply_content":"a",
            "server_id": 1}

    insert_query = "INSERT INTO message_logs (timestamp, user_id, message_content, reply_content, server_id) VALUES (%s, %s, %s, %s, %s)"
    result = cursor.execute(insert_query, (data['timestamp'], data['user_id'], data['message_content'], data["reply_content"], data["server_id"] ))
    print(result)


    db.commit()
    cursor.execute("select * from message_logs;")
    result = cursor.fetchall()
    for row in result:
        print(row)
        print("\n")

    db.commit()
    #close the connection
    db.close()


