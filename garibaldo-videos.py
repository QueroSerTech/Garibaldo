#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup
from pymongo import MongoClient
import urlparse
import requests
import json

# Registra um Log no MongoDB
def mongolog(titulo, canal ,link, categoria):
    client = MongoClient("mongodb://public:public@ds113660.mlab.com:13660/querosertech")
    db = client.querosertech
    return db.playlists.insert_one(
        {   
            "categoria" : categoria,
            "titulo" : titulo,
            "canal" : canal,
            "link" : link
        }
    )

def post(title, link, tag, thumbnail, channel_name, channel_link):
    data = {
        "title" : title, 
        "link"  : link,
        "thumbnail" : thumbnail,
        "channel_name" : channel_name,
        "channel_link" : channel_link,
        "tag" : [
            tag,
            "youtube"
        ]
    }

    headers = {"Content-Type": "application/json"}

    r = requests.post('http://localhost:3000/api/v1/scrapy/videos', data=json.dumps(data), headers=headers)
    print r.json()


#Faz o Crawling no Youtube em busca de canais e playlists
def searchyoutube(termo, categoria):
    query = urllib.quote(termo)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    # Busca por links de Videos
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        videoURL = 'https://www.youtube.com' + vid['href']
        videoTitle = vid['title']

        try:

            #Busca por links dos canais
            videoResponse = urllib2.urlopen(videoURL)
            videoHTML = videoResponse.read()
            videoSOUP = BeautifulSoup(videoHTML, "html.parser")

            #Retorna o nome dos usuarios dos canais
            for canalink in videoSOUP.findAll("a", {'class' : 'yt-user-photo'}):
                canalurl = 'https://www.youtube.com' + canalink['href']
                url_data = urlparse.urlparse(videoURL)
                query = urlparse.parse_qs(url_data.query)
                video_id = query["v"][0]
                video_thumb = "https://img.youtube.com/vi/%s/hqdefault.jpg" % video_id
                print "%s - %s - %s" % (videoTitle, videoURL, video_thumb)

                for image in canalink.findChildren("img"):
                    channel_name = image.get('alt', '')

                post(videoTitle, videoURL, categoria, video_thumb, channel_name, canalurl)

        except:
            print "error to access: %s" % videoURL


def main():

    terms = ["UX", "User Experience", "experiencia do usuario", "ux design"]

    for term in terms:
        searchyoutube(term, term)

        
main()