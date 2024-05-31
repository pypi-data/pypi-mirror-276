import requests
import json 
from datetime import datetime
import uuid
import pytz

now_utcx = datetime.now(pytz.utc)
formatted_timex = now_utcx.strftime("%a, %d %b %Y %H:%M:%S GMT")

def remove_huge_word(prompt, replace_word):
    filtered_prompt = prompt.replace(replace_word, '') 
    return filtered_prompt.strip()

def findmoreinfo(name):
    real_text = name.title()
    if "Enchant" in real_text:
        url = 'https://biggamesapi.io/api/collection/Enchants'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Enchant")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"Enchant | {nameofthething}" in item["configName"]:
                    return item
    if "Charm" in real_text:
        url = 'https://biggamesapi.io/api/collection/Charms'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Charm")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"Charm | {nameofthething}" in item["configName"]:
                    return item
    if "Potion" in real_text:
        url = 'https://biggamesapi.io/api/collection/Potions'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Potion")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"Potion | {nameofthething}" in item["configName"]:
                    return item
    if "Egg" in real_text:
        url = 'https://biggamesapi.io/api/collection/Eggs'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Egg")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    return item
    if "Hoverboard" in real_text:
        url = 'https://biggamesapi.io/api/collection/Hoverboards'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Hoverboard")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    return item
    if "Fruit" in real_text:
        url = 'https://biggamesapi.io/api/collection/Fruits'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Fruit")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    return item
    if "Booth" in real_text:
        url = 'https://biggamesapi.io/api/collection/Booths'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Booth")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    return item
    if "Ultimate" in real_text:
        url = 'https://biggamesapi.io/api/collection/Ultimates'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Ultimate")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    return item
    if "Flag" in real_text:
        url = 'https://biggamesapi.io/api/collection/ZoneFlags'
        response = requests.get(url)
        response_json = response.json()
        RealRealname = remove_huge_word(real_text, "Flag")
        nameofthething = RealRealname.split()[0]
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    return item
    else:
        url = 'https://biggamesapi.io/api/collection/MiscItems'
        response = requests.get(url)
        response_json = response.json()
        nameofthething = real_text
        if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
            data = response_json['data']
            found = False
            for item in data:
                if f"{nameofthething}" in item["configName"]:
                    found = True
                    return item
                if not found:
                    url = 'https://biggamesapi.io/api/collection/Buffs'
                    response = requests.get(url)
                    response_json = response.json()
                    nameofthething = real_text
                    if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
                        data = response_json['data']
                        found = False
                        for item in data:
                            if f"{nameofthething}" in item["configName"]:
                                found = True
                                return item
                            if not found:
                                url = 'https://biggamesapi.io/api/collection/Lootboxes'
                                response = requests.get(url)
                                response_json = response.json()
                                nameofthething = real_text
                                if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
                                    data = response_json['data']
                                    found = False
                                    for item in data:
                                        if f"{nameofthething}" in item["configName"]:
                                            found = True
                                            return item
                                        if not found:
                                            url = 'https://biggamesapi.io/api/collection/RandomEvents'
                                            response = requests.get(url)
                                            response_json = response.json()
                                            nameofthething = real_text
                                            if 'status' in response_json and response_json['status'] == 'ok' and 'data' in response_json:
                                                data = response_json['data']
                                                found = False
                                                for item in data:
                                                    if f"{nameofthething}" in item["configName"]:
                                                        found = True
                                                        return item
                                                    if not found:
                                                        return "NO INFO FOUND"



def getpetvalue(PetName):
    PetName = PetName.replace(' ', '%20')
    PetName = PetName.lower()
    url = f"https://ps99rap.com/api/get/rap?id={PetName}"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "if-modified-since": formatted_timex,
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "theme=dark",
        "Referer": url,
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    result = []
    for entry in data["data"]:
        timestamp = entry[0] / 1000  
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        rap_value = entry[1]
        result.append(f"{date_time} : {rap_value}")
    return result

def getpetexist(PetName):
    PetName = PetName.replace(' ', '%20')
    PetName = PetName.lower()
    url = f"https://ps99rap.com/api/get/exists?id={PetName}"
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": url,
    "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    result = []
    for entry in data["data"]:
        timestamp = entry[0] / 1000  
        date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        rap_value = entry[1]
        result.append(f"{date_time} : {rap_value}")
    return result

def getpetsimilar(PetName):
    PetName = PetName.replace(' ', '%20')
    PetName = PetName.lower()
    url = f"https://ps99rap.com/api/get/similar?id={PetName}"
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": url,
    "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    return data

def ps99invest(PetsName):
    now = datetime.now()
    formatted_timern = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    PetName = PetsName
    PetName = PetName.title()
    rapinfo = f"All rap from Start of data to Today (this is the date and value in gems of each rap data update): {getpetvalue(PetName)}"
    PetExist = f"All exist from Start of data to Today (this is the date and number of exist of each daata update): {getpetexist(PetName)}"
    PetsSimular = f"Pets similar of {PetName} : {getpetsimilar(PetName)}"
    findmoreinfooft = findmoreinfo(PetName)
    prompttt = f"Your name is MaskaV2.Petsim99. Talk like an AI that want to help me and also make your text beatiful, with emojies, alot of different color, make sure your text with hashtag work for a Discord message. My question: Should i invest into the {PetName}, what is the minimal value should i buy it for and the maximal(make sure to look at last value and all the other value. Verify again to see if its make sense and explain why this amount) and what is your value prediction for next month (Also make sure to check if you think the value is fake because sometimes, peoples like manipulating pets to make a fake value of it, so if it got manipulated, start by saying THIS PET IS PROB MANIPULATED with proof of what you know but if value look like a normal value with all the data, say this pet is not Manipulated)(aslo finish by saying, You can also look for this pets because they are similar as your pet .. with the pets similar but don't include image links)? What you know: we are the: {formatted_timern}. Rap: {rapinfo}. Exists: {PetExist}. Similarity: {PetsSimular}. Also add MORE info about the thing. Include Also this info (make sure that the configName is the same as the {PetName} or should almost be the same or you forgot the info that you see): {findmoreinfooft}"
    promptt = f"Max of 900 words, minimum 100 words. If it's a pet then say Pet in the infos, but when it as enchant or potion, Charm or gift or eggs on the name, it's not a pet. it will be a Enchant or a Pet or a Charm or a potion or a egg or a gift. Make sure to verify all info and explain correctly so everyone will understand. Make sure to put color and emoji about each subject and make all the things colorfull. The current Rap is the latest one and the one that the date is the closest to {formatted_timern} and its also the last one of the rap list. Make sure that you put alot of info. Make sure all numbers are good because 90000000 is 90million and 90000000.00 is still 90millions and not 900 millions. Make sure it will get a good looking for discord and try to embed it without a code. one hashtag = giant, two hashtag = mid and 3 hashtag is little for the text on discord. Make sure to not use more then 3 hashtag Last part of prompt: {prompttt}"
    url = "https://api.jarvis.cx/api/v1/ai-chat"
    jarvis_guid = str(uuid.uuid4())
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-jarvis-guid": jarvis_guid,
    "Referer": "https://jarvis.cx/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
    data = {
    "content": promptt,
    "metadata": {
        "conversation": {
            "messages": []
        }
    },
    "model": "gpt-4o" # gpt-3.5-turbo, gpt-4o, gpt-4-turbo, gemini-1.0-pro-latest, gemini-1.5-pro-latest, gemini-1.5-flash-latest
}
    response = requests.post(url, headers=headers, json=data)
    resppppp = json.loads(response.text)
    answer = resppppp["message"]
    if answer == "Internal Server Error":
        return "TRY LATER"
    else: 
        return answer

def aboutcurrentpet():
    url = "https://ps99rap.com/api/get/daily-movers"
    headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": formatted_timex,
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "cookie": "theme=dark",
    "Referer": "https://ps99rap.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  }
    response = requests.get(url, headers=headers)
    maska = response.text
    return maska

def currentPets():
    now = datetime.now()
    formatted_timern = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    aboutcurrentpetopen = aboutcurrentpet()
    prompttt = f"Your name is MaskaV2.Petsim99. Talk like an AI that want to help me and also make your text beatiful, with emojies, alot of different color, make sure your text with hashtag work for a Discord message. My question: What is the current Pets (Put it in different category like: Value going up, Value going down and others stuff like that). What you know: {aboutcurrentpetopen}"
    promptt = f"Max of 800 words, minimum 100 words. If it's a pet then say Pet in the infos, but when it as enchant or potion, Charm or gift or eggs on the name, it's not a pet. it will be a Enchant or a Pet or a Charm or a potion or a egg or a gift. Make sure to verify all info and explain correctly so everyone will understand. Make sure to put color and emoji about each subject and make all the things colorfull. The current Rap is the latest one and the one that the date is the closest to {formatted_timern} and its also the last one of the rap list. Make sure that you put alot of info. Make sure all numbers are good because 90000000 is 90million and 90000000.00 is still 90millions and not 900 millions. Make sure it will get a good looking for discord and try to embed it without a code. one hashtag = giant, two hashtag = mid and 3 hashtag is little for the text on discord. Make sure to not use more then 3 hashtag Last part of prompt: {prompttt}"
    url = "https://api.jarvis.cx/api/v1/ai-chat"
    jarvis_guid = str(uuid.uuid4())
    headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-jarvis-guid": jarvis_guid,
    "Referer": "https://jarvis.cx/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
    data = {
    "content": promptt,
    "metadata": {
        "conversation": {
            "messages": []
        }
    },
    "model": "gpt-4o" # gpt-3.5-turbo, gpt-4o, gpt-4-turbo, gemini-1.0-pro-latest, gemini-1.5-pro-latest, gemini-1.5-flash-latest
}
    response = requests.post(url, headers=headers, json=data)
    resppppp = json.loads(response.text)
    answer = resppppp["message"]
    if answer == "Internal Server Error":
        return "TRY LATER"
    else: 
        return answer
    