import praw 
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import csv


reddit = praw.Reddit(client_id='kOOudQ_moqsYng',
                     client_secret='_HTxk9lyKfOQVS5PyLhR9TzobOI',
                     password='baconlover',
                     user_agent='WordCLoud by /u/dvnielgTCM',
                     username='dvnielgTCM')

sub = input("Which subreddit did you want to visit? (i.e. hiphopheads, worldnews)")

subreddit = reddit.subreddit(sub)
range = input("How many posts do you want to scrape?")

mode = input("How do you want to sort Subreddit? ('new', 'top', 'hot')")
if mode == 'new':
    hot_python = subreddit.new(limit = int(range))
if mode == 'hot':
    hot_python = subreddit.hot(limit = int(range))
if mode == 'top':
    hot_python = subreddit.top(limit = int(range))


posts = []
converted = ''

for submission in hot_python:
    converted+= re.sub(r'[^a-zA-Z ]', "", submission.title) + " "
    converted.lower()

posts = converted.split()
#print(posts)
with open("separate_titles.txt", "w") as output:
    output.write(str(posts))


refined_titles = open('separate_titles.txt').read()
remove_chars = re.sub('[^a-zA-Z0-9\n\.]', ' ', refined_titles)
open('refined_titles.txt', 'w').write(remove_chars)



refined_list = re.sub("[^\w]", " ",  remove_chars).split()
#print (refined_list)

    

count = {}
for w in open('refined_titles.txt').read().split():
    if w in count:
        count[w] += 1
    else:
        count[w] = 1
#for word, times in count.items():
#    print ("%s was found %d times" % (word, times))


with open('badwords.csv', newline='') as f:
    csvread = csv.reader(f)
    stopwords = list(csvread)

i = 0
while i < len(stopwords):
    stopwords[i]= re.sub('[^a-zA-Z0-9\n\.]', ' ', str(stopwords[i])).strip()   
    i+=1
print (list (stopwords))


#apparently you can't remove items from a list while you iterate through them ... took me way too long to figure that out
#but this scans the post titles for any "stopwords" (i.e. the, you, a, and, etc) and removes them

i = 0
while i < len(stopwords):
    j=0
    while j < len(refined_list):
        if stopwords[i] == refined_list[j]:
            refined_list[j] = ''
        j+=1
    i+=1

print (refined_list)


#convert list to string and generate
unique_string=(" ").join(refined_list)
wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig(sub +" wordcloud"+".png", bbox_inches='tight')
plt.show()
plt.close()

