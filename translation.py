import json
import requests
import time
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)
gsheet_url = ""
sh = gc.open_by_url(gsheet_url)

worksheet = sh.worksheet("Trad")
val = worksheet.acell('D2').value
model_id = "Helsinki-NLP/opus-mt-fr-en"
API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


old_val = ""
while True:
    val = worksheet.acell('D2').value
    if old_val != val:
        data = query(val)
        worksheet.update('E2', data[0]["translation_text"])
        old_val = val

