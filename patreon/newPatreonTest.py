import toml
import mysql.connector
import datetime
import json
import patreon

with open('../config.toml', 'r') as f:
    data = toml.load(f)
serverkey = data["serverkey"]

passw = data["dbpsword"]

access_token = data["creatorAccess"] # your Creator Access Token
api_client = patreon.API(access_token)
d = api_client.fetch_user(fields ={"id":"25966444"})

campaign_response = api_client.fetch_campaign()
campaign = campaign_response.data()[0]
# print('campaign is', str(campaign))
# user = campaign.relationship('creator')
# print('user is',str(user)

#Get the campaign ID
campaign_response = api_client.fetch_campaign()
campaign_id = campaign_response.data()[0].id()

# Fetch all pledges
pledges = []
cursor = None
while True:
    pledges_response = api_client.fetch_page_of_pledges(campaign_id, 25, cursor=cursor)
    pledges += pledges_response.data()
    cursor = api_client.extract_cursor(pledges_response)
    if not cursor:
        break
print(json.loads(json.dumps([pledge.json_data for pledge in pledges])))


json_pledges = pledges_response.json_data
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

  # #  myresult = cursor.fetchall()
  #
  #
  #
  #   #query = "SELECT * FROM user_data WHERE user_payment_info = 2;"
  #
  #   #cursor.execute(query)
  #   rows = cursor.fetchall()
  #
  #   print(rows)
  #   #close the connection
  #   db.close()


