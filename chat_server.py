from __future__ import print_function

import time

from absl import app
from absl import flags
from concurrent import futures
import grpc

import chat_pb2
import chat_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

FLAGS = flags.FLAGS
flags.DEFINE_integer('port', 50051, '')


class Messenger(chat_pb2_grpc.MessengerServicer):

  def SendMessage(self, request, context):
    print('Message received from client: %s' % request.message)
    for _ in range(3):
      time.sleep(2)
      yield chat_pb2.MessageReply(message='Hello')


def main(unused_argv):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  chat_pb2_grpc.add_MessengerServicer_to_server(Messenger(), server)
  server.add_insecure_port('[::]:%s' % FLAGS.port)
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  app.run(main)
