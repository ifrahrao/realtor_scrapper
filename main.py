import requests
from bs4 import BeautifulSoup
import json
import csv
import random

all_data=[]
def get_random_user_agent():
    user_agents = [
        "Mozilla/6.0 (Windows NT 9.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/557.36",
        "Mozilla/6.0 (Windows NT 9.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/6.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    return random.choice(user_agents)

def get_data(link):
    session = requests.Session()
    session.headers.update({
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    })
    result={}
    page = session.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    script_tag = soup.find('script', {'type': 'application/json', 'id': '__NEXT_DATA__'})

    if script_tag:
        # Extract the JSON data as a string
        json_data_str = script_tag.string

        # Parse the JSON data
        try:
            json_data = json.loads(json_data_str)

            content=json_data["props"]["pageProps"]["jsonld"]["content"]
            result["firstName"]=content["firstName"]
            result["lastName"] = content["lastName"]
            result["telephone"] = content["telephone"]
            agentDetails=json_data["props"]["pageProps"]["agentDetails"]
            result["address"] = agentDetails["address"]
            result["website"] = agentDetails["office"]["website"]
            result["profile_url"]=link
            all_data.append(result)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("Script tag containing JSON data not found.")

def scrape_real_estates(link):
    session = requests.Session()
    session.headers.update({
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    })
    link_index=0
    new_link=link

    while True:
        try:

            page = session.get(new_link).text
            soup = BeautifulSoup(page, 'html.parser')
            real_estates_info = soup.select('.agent-list-card')
            for real_estate_info in real_estates_info:
                real_estate_info_link = real_estate_info.select('a')[0].get("href")
                get_data("https://www.realtor.com"+real_estate_info_link)
            link_index=link_index+1
            new_link = link + "/pg-" + str(link_index)
        except Exception as e:
            print(e)
            break



def scrape_data(url):
    session = requests.Session()
    session.headers.update({
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    })
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_links=[]
    real_estates = soup.select('.iDsIFW')
    for real_estate in real_estates:
        real_estate_links=real_estate.select('a')
        for real_estate_link in real_estate_links:
            all_links.append("https://www.realtor.com"+real_estate_link.get("href"))
    print(all_links[0])
    for real_links in all_links[:50]:
        scrape_real_estates(real_links)
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url="https://www.realtor.com/realestateagents"
    scrape_data(url)
    with open('realestates.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file,
                            fieldnames=all_data[0].keys(),

                            )
        fc.writeheader()
        fc.writerows(all_data)