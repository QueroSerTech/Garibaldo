# -*- coding: UTF-8 -*-

from google import google
num_page = 3

search_results = google.search("NodeJS Curso Gratis", num_page)

for result in search_results:
    print result.link
    print result.name
