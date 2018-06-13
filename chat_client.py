from __future__ import print_function

import threading
import time

from absl import app
from absl import flags
import grpc

import chat_pb2
import chat_pb2_grpc


FLAGS = flags.FLAGS
flags.DEFINE_integer('port', 50051, '')


def main(unused_argv):
  channel = grpc.insecure_channel('localhost:%s' % FLAGS.port)
  stub = chat_pb2_grpc.MessengerStub(channel)
  responses = stub.SendMessage(chat_pb2.MessageRequest(message='Hello'))

  def func():
    try:
      for response in responses:
        print('Message received from server: %s' % response.message)
    except grpc.RpcError as error:
      print ("RpcError: %s" % error)

  func()

  # t = threading.Thread(target=func)
  # t.daemon = True
  # t.start()

  # while True:
  #   time.sleep(10000)


if __name__ == '__main__':
  app.run(main)
