import grpc
import sys
import os
import unary.unary_pb2_grpc as pb2_grpc1
# from .. import src
# from ..src.unary import unary_pb2_grpc as pb2_grpc2
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3

from unary import unary_pb2_grpc as pb2_grpc
from unary import unary_pb2 as pb2

from google.protobuf.json_format import MessageToDict

class UnaryClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.UnaryStub(self.channel)

    def get_url(self, message):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2.Message(message=message)
        return self.stub.GetServerResponse(message)

    def get_scan(self):
        scan_req = pb2.ScanReq(
            book="/home/sharath/Downloads/books/The Oxford Handbook of Aesthetics (Jerrold Levi... (Z-Library).pdf", 
            start="5", 
            end="5"
        )
        res = self.stub.Scan(scan_req)
        dict_response = MessageToDict(res)
        for i in dict_response['pairs']:
            print(i['word'], i['meaning'])
        return dict_response


if __name__ == '__main__':
    client = UnaryClient()
    result = client.get_scan()