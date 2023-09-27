from PyPDF2 import PdfReader
from wordfreq import zipf_frequency
import re
from sys import stdout as terminal
from time import sleep
import itertools
from itertools import cycle
from threading import Thread
from stemming.porter2 import stem
import nltk
lemma = nltk.wordnet.WordNetLemmatizer()

done = False

def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        terminal.write('\rloading ' + c)
        terminal.flush()
        sleep(0.1)
    terminal.write('\rDone!    ')
    terminal.flush()

def remove_punctuation(text_Lower):
	punctuations = [".", ",", "?", ";", "!", ":", "'", "(", ")", "[", "]", "\"", "...", "-", "~", "/", "@", "{", "}", "*", "’", "‘"]
	punctuations1 = ["-"]
	for i in punctuations1:
		text_Lower = text_Lower.replace(i, " ")
	
	for i in punctuations:
		text_Lower = text_Lower.replace(i, "")
	return text_Lower

book1 = "../../../Downloads/books/Guns, Germs, and Steel The Fates of Human Societies.pdf"
book2 = "../../../Downloads/books/one-hundred-years-of-solitude.pdf"
book3 = "../../../Downloads/books/Emailing Stalingrad-1.pdf"
book4 = "../../../Downloads/books/Frankenstein [full text].pdf"

reader = PdfReader(book3)
number_of_pages = len(reader.pages)





def remove_numbers(variable):
    if (variable.isdigit()):
        return False
    else:
        return True

def getlemma(i):
	ll = lemma.lemmatize(i)
	return ll

def get_vocab(page, n):
	z_dict = {}
	ltt_dict = {}
	text = page.extract_text()
	text_Lower = text.lower()
	text_punct = remove_punctuation(text_Lower)
	text_punct_list = text_punct.split()
	text_punct_list = list(filter(remove_numbers, text_punct_list))
	text_punct_list_stem = [ stem(i) for i in text_punct_list]
	text_punct_list_lemma = [ getlemma(i) for i in text_punct_list]
	for i in range(len(text_punct_list_stem)):
		stemm = text_punct_list_stem[i]
		lemmaa = text_punct_list_lemma[i]
		f_stem = zipf_frequency(stemm, 'en')
		f_lemma = zipf_frequency(lemmaa, 'en')
		if f_lemma>=f_stem and f_lemma <= 3.5 and f_lemma > 0:
			ltt_dict[lemmaa] = f_lemma
		if f_lemma<f_stem and f_stem <= 3.5 and f_stem > 0:
			ltt_dict[stemm] = f_stem
		if f_lemma == 0 :
			z_dict[lemmaa] = f_lemma
	word1 = " ".join(re.findall("[a-zA-Z]+", st))


t = Thread(target=animate)
t.start()
import pathlib
import os
# https://stackoverflow.com/questions/5231901/permission-problems-when-creating-a-dir-with-os-makedirs-in-python
os.makedirs("/directory")
# pathlib.Path('/directory').mkdir(parents=True, exist_ok=True) 
for k in range(number_of_pages):
	page = reader.pages[k]
	get_vocab(page, k)

done = True

# print('########## zero ##########')
# print(z_dict.keys())
# print('########## vocab ##########')
# print(ltt_dict)
def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

# alphanumeral = []
# onlyalpha = []
# for i in ltt_dict:
# 	if has_numbers(i):
# 		alphanumeral.append(i)
# 	else:
# 		onlyalpha.append(i)


# print(onlyalpha)
# print(alphanumeral)