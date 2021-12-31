#Write a function 'scrape_topics' which creates a CSV file of 
# list containing title, topic URL and topic description
#for top featured topics on 'https://github.com/topics' page and returns list of topic_id.

import topics_repositories as tr
from bs4 import BeautifulSoup
import requests
import csv

#function to get topic title
def get_topic_title(a_tag):
    return a_tag.find_all('p')[0].text.strip()

#function to get topic url
def get_topic_url(a_tag):
    base_url = 'https://github.com'
    topic_url = base_url + a_tag['href']
    return topic_url
#function to get topic description
def get_topic_desc(a_tag):
    return a_tag.find_all('p')[1].text.strip()

#function to get topic informations
def get_topic_info(a_tag):
    title = get_topic_title(a_tag)
    topic_url = get_topic_url(a_tag)
    topic_desc = get_topic_desc(a_tag)
    return {
        'Title': title,
        'URL' : topic_url,
        'Desc' : topic_desc
    }

#function to write topics information to csv file
def write_file(items):
    #open a file for write
    
    relative_path = ('D:\python\scraping-github-topics-repositories\\files\\' + 'topics.csv')
    with open(relative_path,'w', encoding= 'utf-8') as file:
        # If no item then return
        if len(items) == 0:
            return 
        
        # Write the header in first line
        headers = list(items[0].keys())
        file.write(','.join(headers) + '\n')
        
        #write all the raw data line by line
        #write one item per line
        
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            file.write(','.join(values) + '\n')

# Function manager where all the other function are getting called and entire flow is made.
def scrape_topics():
    topics_url = 'https://github.com/topics'
    response =  requests.get(topics_url)
    
    # Check if response is successful
    if response.status_code != 200:
        raise Exception('Failed to load webpage "{}"'.format(topics_url))
    #create beautifulsoup object 
    doc = BeautifulSoup(response.text, 'html.parser')
    #create list of a tags
    a_tags = doc.find_all('a', {'class': 'd-flex no-underline'})
    #prepate list of topic informaiton as dictionary
    topic_info = [get_topic_info(tag) for tag in a_tags]
    #function to write data to csv file
    write_file(topic_info)
    return topic_info

#function to scrape each topic
def scrape_all_topics():
    topic_info = scrape_topics()
    for topic in topic_info:
        topic_url = topic['URL']
        topicName = topic_url.split('topics',1)[1]
        topicName = topicName[1:]
        tr.scrape_topic_repositories(topicName)

scrape_all_topics()