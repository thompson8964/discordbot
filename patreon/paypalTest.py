import requests

bearer_token = "A21AAIcBntIr7k0FJ-n1_VVEU6kjbT1d8qlPrbU7nLNv4kMgbNAfbwPq1kGSpxtOqBZsrbyDCsksBOh9T6Vkclbl6VQoDiI0A"

headers = {
    'X-PAYPAL-SECURITY-CONTEXT': '{"consumer":{"accountNumber":1181198218909172527,"merchantId":"5KW8F2FXKX5HA"},"merchant":{"accountNumber":1659371090107732880,"merchantId":"2J6QB8YJQSJRJ"},"apiCaller":{"clientId":"AdtlNBDhgmQWi2xk6edqJVKklPFyDWxtyKuXuyVT-OgdnnKpAVsbKHgvqHHP","appId":"APP-6DV794347V142302B","payerId":"2J6QB8YJQSJRJ","accountNumber":"1659371090107732880"},"scopes":["https://api-m.paypal.com/v1/subscription/.*","https://uri.paypal.com/services/subscription","openid"]}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {bearer_token}',
}

data = '{ "pricing_schemes": [ { "billing_cycle_sequence": 1, "pricing_scheme": { "fixed_price": { "value": "50", "currency_code": "USD" } } }, { "billing_cycle_sequence": 2, "pricing_scheme": { "fixed_price": { "value": "100", "currency_code": "USD" }, "pricing_model": "VOLUME", "tiers": [ { "starting_quantity": "1", "ending_quantity": "1000", "amount": { "value": "150", "currency_code": "USD" } }, { "starting_quantity": "1001", "amount": { "value": "250", "currency_code": "USD" } } ] } } ] }'

response = requests.post('https://api-m.sandbox.paypal.com/v1/billing/plans/P-7GL4271244454362WXNWU5NQ/update-pricing-schemes', headers=headers, data=data)
print(response.json())