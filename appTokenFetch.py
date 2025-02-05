import requests
import json
#ouverture des fichiers
request=open("./authreq.json", "r")
answer=open("./authrep.json", "w")
#requête du token
token=requests.post("http://mafreebox.freebox.fr/api/v5/login/authorize/", data=request.read())
answer.write(token.text)