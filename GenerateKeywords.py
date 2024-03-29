import os
import openai
import re
import requests
from dotenv import load_dotenv
import pyimgur
from rosette.api import API, DocumentParameters, RosetteException
import json

load_dotenv()

#API call to generate keywords in a text
def GenerateKeywordsFromText(prompt: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f'Generate related branding keywords for {prompt}: '
    response = openai.Completion.create(
        engine = 'text-davinci-001', prompt = enriched_prompt, max_tokens = 48
    )
    keywords_text: str = response['choices'][0]['text']
    keywords_text = keywords_text.strip()
    keywords_array = re.split(',|\n|-|;', keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]
    return keywords_array

#API call to generate keywords in a picture
def GenerateKeywordsFromTextBis(prompt: str):
    rosette_api = API(user_key=os.getenv("ROSETTE_API_KEY"))
    keywords_array = []
    params = DocumentParameters()
    params["content"] = prompt
    topics = None
    try:
        topics = rosette_api.topics(params)
        json_obj = json.loads(json.dumps(topics, indent=2, ensure_ascii=False, sort_keys=True))
        for n in json_obj["concepts"]:
            keywords_array.append(n["phrase"].lower())
    except RosetteException as exception:
        print(exception)
        keywords_array = GenerateKeywordsFromText(prompt)
    return keywords_array

#API call to generate keywords in a picture
def GenerateKeywordsFromImage(link: str):
    keywords_array = []
    headers = {"Content-type": "application/x-www-form-urlencoded" , 'api-key':os.getenv("KEYWORDSREADY_API_KEY")}
    response = requests.post('https://keywordsready.com/api/analyzes', {'url':link,  }, headers=headers).json()
    if response["success"] == True:
        for n in response["keywords"]:
            keywords_array.append(n.lower())
    return keywords_array

#upload an picture on imgur
def UploadPicture(path: str):
    im = pyimgur.Imgur(os.getenv("IMGUR_API_KEY"))
    uploadedImage = im.upload_image(path)
    return uploadedImage.link

#removal of unnecessary keywords 
def RemoveUselessKeywords(keywords):
    #bannedkeywords = ["horizon", "people", "color", "image", "emotion"]
    newkeywords = []
    for word in keywords:
        if "horizon" not in word and "people" not in word and "color" not in word and "image" not in word and "emotion" not in word and "travel"  not in word and "adult" not in word and word != "":
            newkeywords.append(word)
    return newkeywords

if __name__ == '__main__':
    #keywords = GenerateKeywordsFromText("Celebrating one's birthday is a special event that's meant to be shared with loved ones. Adults enjoy parties as much as children and it's really nice when people honor your birthday by sharing the day with you. If you are celebrating an important milestone, such as turning 30, 40, 50, or even 60, then it should be celebrated with all the fanfare. A typical birthday party for an adult consists of family and friends, and usually involves a dinner, games, music and much more.")
    #print(keywords)
    link = "https://101funpages.com/wp-content/uploads/2019/12/Birthday-Party00.jpg"
    #link = "https://img-4.linternaute.com/MCcoa60cMU8iyynnXdAvP435vpo=/1500x/smart/c919c40c2d204c2aa8d5648c5c24035f/ccmcms-linternaute/11461924.jpg"
    print(link)
    keywords = GenerateKeywordsFromImage(link)
    print(keywords)
    link = UploadPicture("/Users/nathanfain/Documents/CSC864_Multimedia/media/birthday_2.jpeg")
    #link = UploadPicture("/Users/nathanfain/Documents/CSC864_Multimedia/media/birthday.png")
    print(link)
    keywords = GenerateKeywordsFromImage(link)
    print(keywords)
