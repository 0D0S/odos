from intra import ic

response = ic.get("users", params={"filter[login]": "myko"})
loc = response.json()
print(loc)
