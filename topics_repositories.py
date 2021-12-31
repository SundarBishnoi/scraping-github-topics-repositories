import requests
import os
from bs4 import BeautifulSoup
base_url = 'https://github.com'
import csv

def scrape_topic_repositories(topic, path = None):
    """Get the top repositories for a topic and write them to a CSV file"""

    if path == None:
        path = topic + '.csv'
        relative_path = 'D:\python\scraping-github-topics-repositories\\files\\' + path
    if os.path.exists(path):
        print('The File "{}" Already Exists. Skipping...'.format(path))
        return
    #call function to get topic page
    topic_page = get_topic_page(topic)
    #call function to get information about all repository
    top_repositories = get_top_repositories(topic_page)
    #write all the top repositories information to csv file
    write_csv(top_repositories, relative_path)
    print('Top repositories for topic "{}" is written to file "{}"'.format(topic, path))
    return path
    
    
def get_topic_page(topic):
    #Construct the topic url
    topic_url = 'https://github.com/topics/' + topic
    
    #Download the page using requests.get 
    response = requests.get(topic_url)
    
    #Check if response is successful
    if response.status_code != 200:
        raise Exception("Failed to load webpage, " + topic_url)
    #Construct a beautifulsoup document
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

def parse_star_count(star_str):
    star_str = star_str.strip()
    if star_str[-1] == 'k':
        return int(float(star_str[:-1]) * 1000)
    else : return int(star_str)

def parse_repository(article_tag):
    # Get the <a> tag which has the username, repo_name, URL
    a_tags = article_tag.h3.find_all('a')
    # Owner's username
    username = a_tags[0].text.strip()
    # Repository name
    repo_name = a_tags[1].text.strip()
    # Repository URL
    base_url = 'https:github.com'
    repo_url = base_url + a_tags[1]['href'].strip()
    
    #Star Count
    star_tag = article_tag.find('a', {'class': 'social-count js-social-count'})
    star_count = parse_star_count(star_tag.text.strip())
    
    return {
        'username' : username,
        'repo_name' : repo_name,
        'repo_url' : repo_url,
        'star_count' : star_count
    }

def get_top_repositories(doc):
    article_tags = doc.find_all('article', {'class':'border rounded color-shadow-small color-bg-subtle my-4'})
    topic_repos = [parse_repository(tag) for tag in article_tags]
    return topic_repos

def write_csv(items, path):
    #open a file for write
    with open(path,'w', encoding = 'utf-8') as f:
        # If no item then return
        if len(items) == 0:
            return 
        
        # Write the header in first line
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        
        #write all the raw data line by line
        #write one item per line
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            f.write(','.join(values) + '\n')
