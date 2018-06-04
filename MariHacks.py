import urllib.request
import urllib.error
import shutil
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from nltk.stem import WordNetLemmatizer

index = 7033

##def open_url(url):
##    '''Opens the inputted url and returns the html code in type string.'''
##    response = urllib.request.urlopen(url)
##    html = response.read()
##    html_string = str(html)
##    return html_string

def html_string(index):
    '''Adds on the index to the handspeak url to access words in the dictionary (Max index = 7573). Returns html code in type string.'''
    url = 'https://www.handspeak.com/word/search/index.php?id=' + str(index) 
    response = urllib.request.urlopen(url)
    html = response.read()
    html_string = str(html)
    return html_string

def find_url_extension(html_string):
    '''Reads over the html code from html_string() and returns a sring of a url extension that consists of the first letter of the word and a file with a .mp4 extension.'''
    mp4_index = html_string.find('.mp4') + 3
    file_url_extension = ''
    while 'src' not in file_url_extension:
        file_url_extension = html_string[mp4_index] + file_url_extension
        mp4_index -= 1
    file_url_extension = file_url_extension[5:]
    file_url_extension = file_url_extension.lower()
    return file_url_extension

def download_mp4(file_url_extension):
    '''Takes an extension from the html code and adds in onto the handspeak url. If the file exists, it's downloaded into the current working directory. If the file doesn't exist, the code continues to the next word.'''
    global index
    file_name = file_url_extension.split('/')[-1]
    if file_name[0] == 'a':
        file_url = 'https://www.handspeak.com/' + file_url_extension
        try:
            with urllib.request.urlopen(file_url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except urllib.error.HTTPError:
            with open('missing_indicies.txt', "a") as missing_translations:
                missing_translations.write(str(index))
                index -= 1

def get_translation():
    '''Downloads a single translation video for a given index.'''
    html_useful = html_string(index)
    url_extension = find_url_extension(html_useful)
    download_mp4(url_extension)

def download_all():
    global index
    while index >= 0:
        get_translation()
        index -= 1
        print(index)

##download_all()

lemmatizer = WordNetLemmatizer()

sentence_input = input()
sentence_string = sentence_input.lower()
words = sentence_string.strip('.",!?-=').split()

useless_words_file = open('UselessWords.txt', 'r')
useless_words = str(useless_words_file.read())
cwd = os.getcwd()
clips = []

for word in words:
    if word in useless_words:
        continue
    rootword = lemmatizer.lemmatize(word)
    videofile = rootword + '.mp4'
    try:
        os.chdir(cwd + '\\' + rootword[0])
        test_open_file = open(videofile, 'r')
        test_open_file.close()
        clip = VideoFileClip(videofile)
        clip.set_duration(1)
        clips += [clip]
    except FileNotFoundError:
        useless_words += ' ' + word
        continue

os.chdir(cwd)
useless_words_file.close()
concatenated_clips = concatenate_videoclips(clips, method = 'compose')
concatenated_clips.write_videofile('translation.mp4')
os.startfile('translation.mp4')
