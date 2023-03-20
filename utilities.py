import toml
data = {"gptkey":"YOURCODE",
        "serverkey": "SERVERCODE"
        }

with open('config.toml', 'w') as f:
    toml.dump(data, f)