#THIS IS THE WORKING VERSION OF THE PATREON API.

import patreon
from emailer import emailSender
import toml
with open('../config.toml', 'r') as f:
     data = toml.load(f)
import json
from patreonApiJSONRequeststest import RewardInfo
import pymongo
import requests


class RewardInfo():
    def __init__(self, url: str):
        self.url = url
        self.json = self.get_json_data_from_url()

    def get_json_data_from_url(self) -> dict:
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            data = response.json()

            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}

    def get_tier_title(self) -> str:
        return self.json.get("data", {}).get("attributes", {}).get("title")




myclient = pymongo.MongoClient(data["mongoAddress"])
mydb = myclient["chatbotDB"]
messageLogs = mydb["messageLogs"]
userData = mydb["userData"]

access_token = data["creatorAccess"] # your Creator Access Token
#
#
#

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


serverkey = data["serverkey"]

passw = data["dbpsword"]



list_patronIDs = [pledge.get("relationships", {}).get("patron", {}).get("data", {}).get('id', {}) for pledge in json_pledges.get("data", [])]

print(list_patronIDs)

dict_patronEmails = {}
for item in json_pledges.get("included", []):
    if item.get("type") == "user":
        patronID = item.get("id")
        if patronID in list_patronIDs:
            attributes = item.get("attributes", {})
            email = attributes.get("email")
            dict_patronEmails[patronID] = email

dict_patron_reward_links = {}   # user_id: reward link
rewardLinks = {}

for item in json_pledges.get("data", []):
    user_id = None
    for relationship_name, relationship_value in item.get("relationships", {}).items():
        if relationship_name == "patron":
            user_id = relationship_value.get("data", {}).get("id")
        if relationship_name == "reward":
            reward_link = relationship_value.get("links", {}).get("related")
            rewardLinks[user_id] = reward_link
    dict_patron_reward_links[user_id] = reward_link

print(f"dict_patron_reward_links: {dict_patron_reward_links}")

#todo store user paid amount and currency type


# data = json.loads(json.dumps([pledges_response.json_data]))
# email = data[0]["included"][0]["attributes"]["email"]
# pledges_response -> 'included' -> 00 -> 'email'

for patronID, email in dict_patronEmails.items():
    print(email)
    print(patronID)
    result: dict = userData.find_one({"patreonId": patronID})
    if result:
        print(f"Patron already found in database: {patronID}")
    else:
        print("New patron detected! Inserting into database")
        code = emailSender(email) #emailSender will return the verification code




        reward = RewardInfo(rewardLinks[patronID])
        tier = reward.json["data"]["attributes"]["title"]

        data = {"patreonId": patronID,
                "discordId": "",
                "email": email,
                "tier": tier,
                "verifcode": code,
                "tokensLeft": 300,
                "requestsLeft": 10,
                }
        result = userData.insert_one(data)
        print(f"Successfully inserted one record: {result.inserted_id}")
        print(data)


# insert_query = f"INSERT INTO user_patreon_info (discord_id, patreon_id, verif_code) VALUES (%s, %s, %s)"
# data = {"discord_id": 0,# placeholder
#         'patreon_id': list_patronIDs[0],
#         "verif_code": code
#         }


# cursor.execute(insert_query, (
#     data['user_id'], data['user_payment_info'], data['user_tokens'], data["user_requests"]))
# db.commit()
