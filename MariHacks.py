#Take sentence as astring input
#split the sentence
#remove the useless words
#identify word classes
    #take conjugated words and recognize root words
#fetch video files

import urllib.request
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

sentence_input = input()            # input sentence
sentence_string = sentence_input.lower()
words = sentence_string.strip('.",!?-=').split()        # split sentence into lists

##response = urllib.request.urlopen('http://wordnetweb.princeton.edu/perl/webwn?s=running&sub=Search+WordNet&o2=&o0=1&o8=1&o1=&o7=&o5=&o9=&o6=&o3=&o4=&h=0000000000000000000000000000000000000000000000000000')
##html = response.read()
##html_str = str(html)
##print(html_str)
##print(html_str.find('running'))
#The quick brown fox jumps over the lazy brown dog

useless_words_file = open('UselessWords.txt', 'r')
useless_words = str(useless_words_file.read())
##translation = VideoFileClip(word[0] + '.mp4')
##translation_file = VideoFileClip('translation.mp4')
cwd = os.getcwd()
clips = []          # list for clips

for word in words:
    if word in useless_words:
        continue
    videofile = word + '.mp4'
    print(videofile)
    try:
        os.chdir(cwd + '\\' + word[0])
        test_open_file = open(videofile, 'r')
        test_open_file.close()
        clip = VideoFileClip(videofile)
        clips += [clip]
    except FileNotFoundError:
        useless_words += ' ' + word
        continue

os.chdir(cwd) 
useless_words_file.close()          # close file
clips_fixed_duration = [TextClip(txt, fontsize=170, color='green', size=(500,300)).set_duration(1) for txt in clips]

concatenated_clips = concatenate_videoclips(clips, method='compose')
##os.remove('translation.mp4')
concatenated_clips.write_videofile('translation.mp4')
