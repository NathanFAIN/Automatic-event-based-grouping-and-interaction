import os
import openai
import re
import requests
from dotenv import load_dotenv
import pyimgur

load_dotenv()

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

def GenerateKeywordsFromImage(link: str):
    headers = {"Content-type": "application/x-www-form-urlencoded" , 'api-key':os.getenv("KEYWORDSREADY_API_KEY")}
    response = requests.post('https://keywordsready.com/api/analyzes', {'url':link,  }, headers=headers).json()
    if response["success"] == True:
        return response["keywords"]
    return []

def UploadPicture(path: str):
    im = pyimgur.Imgur(os.getenv("IMGUR_API_KEY"))
    uploadedImage = im.upload_image(path)
    return uploadedImage.link

#keywords = GenerateKeywordsFromText("Celebrating one's birthday is a special event that's meant to be shared with loved ones. Adults enjoy parties as much as children and it's really nice when people honor your birthday by sharing the day with you. If you are celebrating an important milestone, such as turning 30, 40, 50, or even 60, then it should be celebrated with all the fanfare. A typical birthday party for an adult consists of family and friends, and usually involves a dinner, games, music and much more.")
#print(keywords)
#keywords = GenerateKeywordsFromImage("https://img-4.linternaute.com/MCcoa60cMU8iyynnXdAvP435vpo=/1500x/smart/c919c40c2d204c2aa8d5648c5c24035f/ccmcms-linternaute/11461924.jpg")
#print(keywords)