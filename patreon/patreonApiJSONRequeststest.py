import requests
import json


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


if __name__ == "__main__":  # the following code will only run when you run this script directly
    url = "https://www.patreon.com/api/rewards/9902618"
    reward_info = RewardInfo(url=url)
    print(reward_info.get_tier_title())

    # todo get tier, user id, email, and send to sql db

    print("All done!")

