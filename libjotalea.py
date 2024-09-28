# pip install aiohttp
# pip install requests
# pip install discord

GPT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
GPT_KEY = ""
GPT_HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {GPT_KEY}"}
GPT_MODEL = "gpt-4"
GPT_TTS_URL = ""
GEMINI_KEY = ""

def gemini(prompt, uRequests:bool=False):
    # curl -H 'Content-Type: application/json' -d '{"contents":[{"parts":[{"text":"Write a story about a magic backpack"}]}]}' -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY
    import os
    if uRequests:
        import requests
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        params = {
            'key': GEMINI_KEY
        }
        response = requests.post(url, headers=headers, json=data, params=params)

        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_KEY)

        model = genai.GenerativeModel('models/gemini-pro')
        chat = model.start_chat()
        try:
            response = chat.send_message(prompt)
        except Exception as e:
            return f"Your message was blocked:\n{e}"

        print(response.text)
    
        return response.text

def chatgpt(prompt:str, history_payload:list):
    import requests, json
    global GPT_ENDPOINT, GPT_HEADERS, GPT_KEY, GPT_MODEL, GPT_TTS_URL, payload, data

    payload = [
        {"role": "system", "content": "You are a helpful AI."},
        {"role": "user", "content": prompt}
    ]

    data = {
        "model": GPT_MODEL,
        "messages": history_payload + [{"role": "user", "content": prompt}]
    }

    try:
        if GPT_ENDPOINT == "https://api.openai.com/v1/chat/completions":
            response = requests.post(GPT_ENDPOINT, headers=GPT_HEADERS, data=json.dumps(data))
        else:
            response = requests.post(GPT_ENDPOINT, headers=GPT_HEADERS, json=data)
        return response.json()
    except Exception as e:
        return e

def tts(text, api_key):
    import requests
    api_domain = "api.shuttleai.app"
    url = f"https://{api_domain}/v1/audio/speech"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "eleven-labs",
        "input": text,
        "voice": "james"
    }

    import random

    random_v = random.randint(1000000, 9999999)
    
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.content)
    
    response_a = requests.get(response.content)

    with open(f"/files/speech_{random_v}.png", "wb") as file:
        file.write(response_a)

    path = "/files/speech_{random_v}.mp3"
#    with open(f"/files/speech{random_v}.mp3", "rb") as file:
#        file_send = file.read()
#    return file_send
    return path

def ttsmp3(text, voice:str="Enrique"):
    import requests, json
    response = requests.post("https://ttsmp3.com/makemp3_new.php", data={"msg":text,"lang":voice,"source":"ttsmp3"})
    mp3 = json.loads(response.text)
    return f"https://ttsmp3.com/created_mp3/{mp3['MP3']}"

def webhook(url:str, content:str="Test content", debug:bool=False):
    import requests
    try:
        rs = requests.post(url, json={"content": content})
        if rs.status_code == 200:
            return True
    except Exception as e:
        if debug:
            return str(e)
        else:
            return False

async def async_webhook(url: str, content: str = "Test content", debug: bool = False):
    import aiohttp, asyncio, json
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"content": content}) as response:
                if response.status == 200:
                    return True
                else:
                    if debug:
                        return response.status
                    return False
    except Exception as e:
        if debug:
            return str(e)
        return False

log = []

def ansirgb(r:int=0, g:int=0, b:int=0):
    return f"\x1b[38;2;{r};{g};{b}m"

def gradient(text:str, mode:str, start_color:list, end_color:list, usenumpy:bool=False):
    # If usenumpy is True, the numpy module is required.
    
    # Example usage:
    # gradient(text="Text", mode="by-character-diagonal", start_color=[0, 0, 0], end_color=[255, 255, 255])

    # Notes:
    # text          must be a string        any content
    # mode          must be a string        its content can only be "by-character", "by-character-diagonal", "line-horizontal" or "line-vertical"
    # start_color   must be a list          its content must be [int>0<255, int>0<255, int>0<255]
    # end_color     must be a list          its content must be [int>0<255, int>0<255, int>0<255]
    # usenumpy      must be a bool          its content must be True (default) or False
    
    class InvalidRGBColor(Exception):
        def __init__(self, reason=None):
            self.reason = reason
            message = "The RGB value must be higher than 0 and lower than 255. Your input doesn't match those requirements."
    
    class InvalidGradientOption(Exception):
        def __init__(self, reason=None):
            self.reason = reason
            message = f"The gradient option you chose ({str(reason)}) is not a valid option."
    
    class InvalidStepsAmount(Exception):
        def __init__(self, reason=None):
            self.reason = reason
            message = "The amount of steps for the gradient must be integer and higher than 0."
    
    def rgb(r:int=0, g:int=0, b:int=0):
        return f"\x1b[38;2;{r};{g};{b}m"
    
    def generate_rgb_grad(start_color, end_color, steps, un=usenumpy):

        def validate_rgb_color(color):
            for channel in color:
                if not 0 < channel < 255:
                    raise InvalidRGBColor("RGB color values should be between 0 and 255")
        
        validate_rgb_color(start_color)
        validate_rgb_color(end_color)
        
        if un:
            try:
                import numpy as np
            except ImportError:
                import sys
                import platform
                
                if platform.system() == "Windows":
                    python_command = "python"  # Windows ussually has Python in PATH
                else:
                    python_command = sys.executable or "python"
                
                print(f"Numpy module is not installed.\nInstall it by running \"{python_command} -m pip install numpy\" or disable it.")
            if steps <= 0:
                raise InvalidStepsAmount("The amount of steps must be higher than 0")
            s_color = np.array(start_color)
            e_color = np.array(end_color)
            delta_color = (e_color - s_color) / steps
            gradient = np.round(np.arange(steps + 1)[:, np.newaxis] * delta_color + s_color).clip(0, 255).astype(int)
            return gradient.tolist()
        else:
            if steps <= 0:
                raise InvalidStepsAmount("The amount of steps must be higher than 0")
            # Calculate the difference between the start and the end values for each RGB component
            delta_r = (end_color[0] - start_color[0]) / steps
            delta_g = (end_color[1] - start_color[1]) / steps
            delta_b = (end_color[2] - start_color[2]) / steps
            # Generate the gradient
            gradient = []
            for i in range(steps + 1):
                # Calculate the RGB values for the current step
                r = round(start_color[0] + i * delta_r)
                g = round(start_color[1] + i * delta_g)
                b = round(start_color[2] + i * delta_b)
                # Make sure the values are in range [0, 255]
                r = min(255, max(0, r))
                g = min(255, max(0, g))
                b = min(255, max(0, b))
                # Add the values to the gradient list
                gradient.append([r, g, b])
            return gradient
        
    if mode == "by-character":
        t = list(text)
        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=len(t)-1)
        i = 0
        for character in t:
            print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
            i = i + 1
    elif mode == "by-character-diagonal":
        t = list(text)
        if "\n" in t:
            li = text.split("\n")
        t.append("\n")
        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=(len(text.split("\n")[0]) + text.count("\n")) if (text and "\n" in text) else None)
        i = 0
        o = 0
        if li:
            for line in li:
                i = i + o
                for character in line:
                    print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                    i = i + 1
                o = o + 1
                if o < len(li):
                    print("\033[0m", end='\n')
                    i = 0
        else:
            for character in t:
                print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                i = i + 1
    elif mode == "line-vertical":
        t = list(text)
        if "\n" in t:
            li = text.split("\n")
        t.append("\n")
        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=(len(text.split("\n")[0]) + text.count("\n")) if (text and "\n" in text) else None)
        i = 0
        o = 0
        if li:
            for line in li:
                for character in line:
                    print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                    i = i + 1
                o = o + 1
                if o < len(li):
                    print("\033[0m", end='\n')
                    i = 0
        else:
            for character in t:
                print(f"{rgb(l[i][0], l[i][1], l[i][2])}{character}", end='')
                i = i + 1
    elif mode == "line-horizontal":
        t = text.split("\n")

        # Remove the last "\n"
        tc = len(t) - 1
        c = 0
        tt = []
        while tc > 0:
            tt.append(t[c])
            c += 1
            tc += -1
        t = tt

        s_color = list(start_color)
        e_color = list(end_color)
        l = generate_rgb_grad(start_color=s_color, end_color=e_color, steps=len(t)-1)
        i = 0
        for line in t:
            print(f"{rgb(l[i][0], l[i][1], l[i][2])}{line}", end='\n')
            i = i + 1
    else:
        raise InvalidGradientOption("The gradient option you chose (%s) doesn't exist." % mode)
    
    # End any remaining color
    print("\033[0m", end='')

def prettyprint(color, text):
    global outcolor
    if color == "red":
        outcolor = "\033[31m"
    elif color == "green":
        outcolor = "\033[32m"
    elif color == "yellow":
        outcolor = "\033[33m"
    elif color == "blue":
        outcolor = "\033[34m"
    elif color == "purple":
        outcolor = "\033[35m"
    elif color == "cyan":
        outcolor = "\033[36m"
    elif color == "white":
        outcolor = "\033[37m"
    else:
        outcolor = "\033[0m"  # Default
    print(outcolor + str(text) + "\033[0m")
    return

async def old_tts(ttsText, download=False, upload=False, uplURL="https://example.com"):
    import aiohttp

    # Request for TTS generation
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {GPT_KEY}'}) as session:
        async with session.post(GPT_TTS_URL, json={'text': ttsText}) as resp:
            response = await resp.json()

    ttsURL = response["url"]

    if upload == False:
        return ttsURL

    if download:
        async with aiohttp.ClientSession() as session:
            async with session.get(ttsURL) as audio_response:
                if audio_response.status == 200:
                    audio_data = await audio_response.read()
                    with open('ai_tts.mp3', 'wb') as audio_file:
                        audio_file.write(audio_data)

    if upload:
        import os
        # Send the downloaded TTS audio file as an attachment
        with open('ai_tts.mp3', 'rb') as audio_file:
            pass # UPLOAD API GOES HERE
        os.remove('ai_tts.mp3')
    return

def getIP(returnIP:bool=True,returnLoc:bool=True,returnCoords:bool=True,returnAll:bool=False):
    import requests, json, os
    # g=lambda r,l,c,a:json.dumps({k:v for k,v in requests.get('https://ipinfo.io/json').json().items() if k in ["ip","loc"]+["country","region","city"]*(l-1)+(a-1)*["country","region","city"]}) if r or l or c or a else ""
    data = requests.get('https://ipinfo.io/json').json()
    r = ""
    if returnIP:
        r = r + str(data["ip"])
        pass
    if returnLoc:
        r = r + str(data["country"]) + ", " + str(data["region"]) + ", " + str(data["city"])
        pass
    if returnCoords:
        r = r + str(data["loc"])
        pass
    if returnAll:
        r = str(f"IP: {data['ip']}\nUser: {os.getlogin()}\nCity: {data['city']}\nState: {data['region']}\nCountry: {data['country']}\nCoords: {data['loc']}\nZIP Code: {data['postal']}\nTimezone: {data['timezone']}")
        pass
    return r
