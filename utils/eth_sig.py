import requests
import json


#4byte.directory API
def get_function_name(signature):
    url = "https://www.4byte.directory/api/v1/signatures/?hex_signature=" + signature
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        if data['results'] != []:
            sorted_results = sorted(data['results'], key=lambda x: x['created_at'])
            print(sorted_results[0]['text_signature'])
            return sorted_results[0]['text_signature']
        else:
            ("No func name for %s" % signature)
    else:
        print("Error: %s" % response.status_code)
        return None

#openchain.xyz
def get_function_name2(signature):
    url = "https://api.openchain.xyz/signature-database/v1/search?query=" + signature
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        if len(data['result']['function']) != 0 :
            print("Function name: %s" % data['result']['function'][0]['name'])
            return data['result']['function'][0]['name']
        