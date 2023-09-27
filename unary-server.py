import grpc
from concurrent import futures
import time
import unary.unary_pb2_grpc as pb2_grpc
import unary.unary_pb2 as pb2
from wordfreq import zipf_frequency


class UnaryService(pb2_grpc.UnaryServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        # get the string from the incoming request
        f = zipf_frequency('the', 'en')
        print(f)
        message = request.message
        result = f'Hello I am up and running received "{message}" message from you'
        result = {'message': result, 'received': True}
        return pb2.MessageResponse(**result)
    
    def GetWordFrequencies(self, request, context):
        
        words = request.words        
        freq = []
        print(words)
        for w in words:
            f = zipf_frequency(w, 'en')
            freq.append(f)

        print('freq --> ', freq)
        result = {
            "frequencies": freq
        }
        return pb2.Frequencies(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # add services to the server
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()