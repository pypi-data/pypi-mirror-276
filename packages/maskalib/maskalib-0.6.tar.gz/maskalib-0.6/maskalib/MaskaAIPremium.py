import requests
import json
from datetime import datetime, timezone
import base64

def big_api_key_to_text(big_api_key):
    big_api_key = big_api_key.replace("MaskaAI-", "")
    combined = base64.urlsafe_b64decode(big_api_key)

    salt = combined[:32]
    text_bytes = combined[32:]

    decoded_str = text_bytes.decode('utf-8')
    return decoded_str

def extract_date_and_status(prompt):
    parts = prompt.split('+')

    status = parts[1] if len(parts) > 1 else None
    date = parts[2] if len(parts) > 2 else None

    return status, date

def compare_dates(input_date_str):
    today_date = datetime.today().strftime('%m/%d/%Y')

    input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
    today_date_obj = datetime.strptime(today_date, '%m/%d/%Y')

    if input_date == today_date_obj:
        return False
    elif input_date < today_date_obj:
        return False
    else:
        return True

def MaskaAIPremium(Model2, AINAME, MessageAsk, APIKEY):
    api_dev_key = 'DE2MZS4SwAR8Q0QpOqVZbFIShyxtSt_p'
    api_user_key = 'e58b7312c20218ec7fc2c3277b03fa2c'
    url = 'https://pastebin.com/api/api_raw.php'
    payload = {
    'api_option': 'show_paste',
    'api_user_key': api_user_key,
    'api_dev_key': api_dev_key,
    'api_paste_key': 'kcGN0nWL'}
    response = requests.post(url, data=payload)
    data = response.text
    if APIKEY in response.text:
        reverted_text = big_api_key_to_text(APIKEY)
        status, date = extract_date_and_status(reverted_text)
        resultDate = compare_dates(date)
        if status == "Premium":
            if resultDate == False:
                return ["Key is expired","Key is expired","Key is expired"]
            else:
                pass
        else:
            return ["You need to buy Premium First","You need to buy Premium First","You need to buy Premium First"]
    else: 
        return ["Key Doesnt Exist", "Key Doesnt Exist","Key Doesnt Exist"]
    
    if Model2 == "MaskaAI":
        Model = "CohereForAI/c4ai-command-r-plus"
    if Model2 == "FibiAI":
        Model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    if Model2 == "ScenarioAI":
        Model = "01-ai/Yi-1.5-34B-Chat"
    if Model2 == "GoogleAI":
        Model = "google/gemma-1.1-7b-it"
    if Model2 == "MicroAI":
        Model = "microsoft/Phi-3-mini-4k-instruct"
    else:
        Model = "CohereForAI/c4ai-command-r-plus"
    current_utc_time = datetime.now(timezone.utc)
    formatted_utc_time = current_utc_time.strftime('%Y-%m-%d %H:%M:%S UTC')
    Textinput = MessageAsk
    whatyouknow = f"Act like an AI assistant called {AINAME}. This is what you know but don't tell it if I didn't ask. Don't say 'like MaskAI:...' because you are the MaskaAI. Right now we are at {formatted_utc_time}. My Question: {Textinput}"
    newchatfoundurl = "https://huggingface.co/chat/settings"
    headersxxxx = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Opera GX\";v=\"109\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://huggingface.co/chat/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    datadxxxxxxxxxxx = {"searchEnabled": True, "ethicsModalAccepted": False, "ethicsModalAcceptedAt": None, "activeModel": f"{Model}", "hideEmojiOnSidebar": False, "shareConversationsWithModelAuthors": True, "customPrompts": {}, "assistants": [], "tools": {}, "recentlySaved": False}
    rsesaxadsad = requests.post(newchatfoundurl, headers=headersxxxx, json=datadxxxxxxxxxxx)
    gfjdgdfgkjdf = rsesaxadsad.headers
    newnewhfchat = gfjdgdfgkjdf["X-Amz-Cf-Id"]
    hfchat = str(newnewhfchat)
    uxl = f"https://huggingface.co/chat/models/{Model}/__data.json?x-sveltekit-invalidated=11"
    headersx = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Opera GX\";v=\"109\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"hf-chat={hfchat}",
        "Referer": f"https://huggingface.co/chat/models/{Model}",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    xrepsons = requests.post(uxl, headers=headersx)
    url = "https://huggingface.co/chat/conversation"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Opera GX\";v=\"109\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"hf-chat={hfchat}",
        "Referer": f"https://huggingface.co/chat/models/{Model}",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    data = {"model": f"{Model}"}
    response = requests.post(url, headers=headers, json=data)
    jsons = json.loads(response.text)
    jsonsx = jsons["conversationId"]
    url1 = f"https://huggingface.co/chat/conversation/{jsonsx}/__data.json?x-sveltekit-invalidated=11"
    headers1 = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": "\"Opera GX\";v=\"109\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"hf-chat={hfchat}",
        "Referer": f"https://huggingface.co/chat/models/{Model}",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    response1 = requests.get(url1, headers=headers1)
    jsons1 = json.loads(response1.text)
    jsonsx1 = jsons1["nodes"][1]["data"][3]
    newnewurl = f"https://huggingface.co/chat/conversation/{jsonsx}"
    newnewheaders = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Opera GX\";v=\"109\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": f"hf-chat={hfchat}",
        "Referer": f"https://huggingface.co/chat/conversation/{jsonsx}",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    datanewnew = {"inputs": f"{whatyouknow}", "id": f"{jsonsx1}", "is_retry": False, "is_continue": False, "web_search": True, "tools": {}, "files": []}
    resss = requests.post(newnewurl, headers=newnewheaders, json=datanewnew)
    response_objects = resss.text.split('\n')
    result = []

    for obj in response_objects:
        if obj.strip():
            try:
                data = json.loads(obj)
                if "type" in data:
                    if data["type"] == "status":
                        result.append(data["status"])
                    elif data["type"] == "title":
                        titlexx = data["title"]
                        last_dot_index = titlexx.rfind('.')
                        if last_dot_index != -1:
                            result.append(titlexx[:last_dot_index + 1])
                        else:
                            result.append(data["title"])
                    elif data["type"] == "finalAnswer":
                        result.append(data["text"])
            except json.JSONDecodeError as e:
                pass
    return result