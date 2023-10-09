import sys
from sys import stdout as terminal
import grpc
from concurrent import futures
import time
import os
# print(os.getcwd())
sys.path.append(os.getcwd()) # why are we doing this
import src.unary.unary_pb2_grpc as pb2_grpc
import src.unary.unary_pb2 as pb2

from PyPDF2 import PdfReader
from wordfreq import zipf_frequency
import re
import pathlib
import os
from time import sleep
import itertools
from itertools import cycle
from threading import Thread
from stemming.porter2 import stem
import nltk
lemma = nltk.wordnet.WordNetLemmatizer()
import src.unaryservice as unaryservice


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=(('grpc.so_reuseport', 0),))
    sys.stdout.flush()
    pb2_grpc.add_UnaryServicer_to_server(unaryservice.UnaryService(), server)
    sys.stdout.flush()
    
    server.add_insecure_port('[::]:50051')
    sys.stdout.flush()
    
    server.start()
    sys.stdout.flush()
    
    server.wait_for_termination()


if __name__ == '__main__':
    serve()