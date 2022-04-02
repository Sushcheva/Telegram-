import requests as req

resp = req.get("https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=40d1649f-0493-4b70-98ba-98533de7710b")
print(resp.json())