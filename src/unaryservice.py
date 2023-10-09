import sys
from sys import stdout as terminal
import grpc
from concurrent import futures
import time
import src.unary.unary_pb2_grpc as pb2_grpc
import src.unary.unary_pb2 as pb2

from PyPDF2 import PdfReader
from wordfreq import zipf_frequency
import re
import pathlib
from pathlib import Path
import os
from time import sleep
import itertools
from itertools import cycle
from threading import Thread
from stemming.porter2 import stem
import nltk
lemma = nltk.wordnet.WordNetLemmatizer()

class UnaryService(pb2_grpc.UnaryServicer):

    def __init__(self, *args, **kwargs):
        print('initialized unary service')
        pass

    def GetServerResponse(self, request, context):
        # get the string from the incoming request
        f = zipf_frequency('the', 'en')
        message = request.message
        result = f'Hello I am up and running received "{message}" message from you'
        result = {'message': result, 'received': True}
        return pb2.MessageResponse(**result)
    
    def GetWordFrequencies(self, request, context):    
        words = request.words        
        freq = []
        for w in words:
            f = self.zipf_frequency(w, 'en', wordlist='large')
            freq.append(f)
        result = {
            "frequencies": freq
        }
        return pb2.Frequencies(**result)
    
    def remove_punctuation(self, text_Lower):
        punctuations = [".", ",", "?", ";", "!", ":", "'", "(", ")", "[", "]", "\"", "...", "-", "~", "/", "@", "{", "}", "*", "’", "‘"]
        punctuations1 = ["-"]
        for i in punctuations1:
            text_Lower = text_Lower.replace(i, " ")
        
        for i in punctuations:
            text_Lower = text_Lower.replace(i, "")
        return text_Lower

    def create_folder_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def remove_numbers(self, variable):
        if (variable.isdigit()):
            return False
        else:
            return True

    def getlemma(self, i):
        ll = lemma.lemmatize(i)
        return ll

    def get_word_meaning(self, word):
        synsets = nltk.corpus.wordnet.synsets(word)
        meanings = None
        if synsets:
            meanings = []
            for synset in synsets:
                meanings.append([word, synset.definition()])
        return meanings

    def getpages(self, arg):
        pattern = r'(^[0-9]+)-?([0-9]*)'
        matches = re.findall(pattern, arg)
        def int_or_zero(s):
            if s == '':
                return 0
            else:
                return int(s)
        pageone = self.int_or_zero(matches[0][0])
        pagetwo = self.int_or_zero(matches[0][1])
        if pageone <= pagetwo:
            pass
        elif pagetwo > pageone :
            pagetwo = pageonoe
        return [pageone, pagetwo]

    def get_vocab(self, page, n):
        z_dict = {}
        ltt_dict = {}
        text = page.extract_text()
        text_Lower = text.lower()
        text_punct = self.remove_punctuation(text_Lower)
        text_punct_list = text_punct.split()
        text_punct_list = list(filter(self.remove_numbers, text_punct_list))
        text_punct_list_stem = [ stem(i) for i in text_punct_list]
        text_punct_list_lemma = [ self.getlemma(i) for i in text_punct_list]
        for i in range(len(text_punct_list_stem)):
            stemm = text_punct_list_stem[i]
            lemmaa = text_punct_list_lemma[i]
            f_lemma = 0
            f_stem = 0
            try:
                f_stem =  zipf_frequency(stemm, 'en',  wordlist='large')
            except Exception as e:
                f_stem = 2
                print(f"An error occurred: getting frequency of the word {text_punct_list[i]}", str(e))
            try:
                f_lemma = zipf_frequency(lemmaa, 'en',  wordlist='large')
            except Exception as e:
                f_stem = 2
                print(f"An error occurred: getting frequency of the word {text_punct_list[i]}", str(e))

            if f_lemma>=f_stem and f_lemma <= 3.5 and f_lemma > 0:
                ltt_dict[lemmaa] = f_lemma
            if f_lemma<f_stem and f_stem <= 3.5 and f_stem > 0:
                ltt_dict[stemm] = f_stem
            if f_lemma == 0 :
                z_dict[lemmaa] = f_lemma
        meanings_list = []
        for i in ltt_dict:
            meanings = self.get_word_meaning(i)
            if meanings != None:
                meanings_list.extend(meanings)
        return meanings_list

    def Scan(self, request, context):
        sys.stdout.flush()
        book = request.book
        page1 = int(request.start) - 1
        page2 = int(request.end) - 1
        book4 = book
        reader = PdfReader(book4)
        folder_path = "vocabdir"
        self.create_folder_if_not_exists(folder_path)
        pages = [page1, page2]
        vl = []
        for k in range(pages[0], pages[1]+1):
            page = reader.pages[k]
            v = self.get_vocab(page, k)
            vl.extend(v)
        vl = [{'word': i[0], 'meaning': i[1]} for i in vl]
        result = {
            "pairs": vl
        }
        k = pb2.ScanRes(**result)
        return k

