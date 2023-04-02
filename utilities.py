import toml
data = {'gptkey': "YOURKEY",
        'serverkey': "YOURKEY",
        'exitKey': "YOURKEY",
}

with open('config.toml', 'w') as f:
    toml.dump(data, f)