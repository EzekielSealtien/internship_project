import requests
url = "http://localhost:8000/user/get_user_full_info"
email={"email":"takam@gmail.com"}
response = requests.get(url,params=email)

print("Response------------>:", response.json())
