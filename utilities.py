import toml
data = {"gptkey":"YOURKEY",
        "serverkey": "YOURCODE",
        "exitKey": "YOURPASSWORD"
        }

with open('config.toml', 'w') as f:
    toml.dump(data, f)