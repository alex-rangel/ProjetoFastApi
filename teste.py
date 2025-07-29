import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzUzNzQ3MTY0fQ.MH1Sj17fdbFu1AL47G4vCCXn7RZh7AreosasxJRczD0"
}

requisicao = requests.get("http://127.0.0.1:3000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())