#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
from bs4 import BeautifulSoup
from pymongo import MongoClient

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

def post(titulo, link, categoria):
    pass


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

        #Busca por links dos canais
        videoResponse = urllib2.urlopen(videoURL)
        videoHTML = videoResponse.read()
        videoSOUP = BeautifulSoup(videoHTML, "html.parser")

        # Retorna o nome dos usuarios dos canais
        for canalink in videoSOUP.findAll("a", {'class' : 'yt-user-photo'}):
            canalurl = 'https://www.youtube.com' + canalink['href']

            #print canalurl
            playlistsUrl = canalurl + "/playlists"

            # Busca pelo nome e link das playlists
            playlistsResponse = urllib2.urlopen(playlistsUrl)
            playlistsHTML = playlistsResponse.read()
            playlistsSOUP = BeautifulSoup(playlistsHTML, "html.parser")

            try:
                for playlist in playlistsSOUP.find("ul", {"id" : "channels-browse-content-grid"}).findAll("a", {"class" : "yt-uix-tile-link"}):
                    print  playlist["title"] + " - " + 'https://www.youtube.com' + playlist["href"]
                    ##mongolog(playlist["title"], playlistsUrl ,'https://www.youtube.com' + playlist["href"], categoria)
            except:
                pass


def main():

    terms = ["UX", "User Experience", "experiencia do usuario", "ux design"]

    for term in terms:
        searchyoutube(term, term)
        #searchyoutube("Tutorial de " + term + " PT", term)

main()




