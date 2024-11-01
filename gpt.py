from openai import OpenAI
import os
from dotenv import load_dotenv 
load_dotenv() 

def field_finder(html, desired_contents):
    client = OpenAI(
        api_key=os.getenv("API_KEY")
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Your task is to help users identify relevant information to scrape from provided HTML content. You will: 1. Analyze the HTML to find elements based on the user's request. 2. List class names of matching elements and nothing else. 3. Only return a dictionary with the keys being the list of desired fields and values being a string of the matched element and nothing else. For example, If they ask for 'price,' identify class names related to pricing, and return all class names related to that."},
            {"role": "user", "content": f"find feilds in provided html that match this list of feilds. list:{desired_contents} html:{html}"}
        ],
        response_format={ "type": "json_object" },

    )
    
    return completion.choices
 