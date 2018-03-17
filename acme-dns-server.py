#!/usr/bin/env python3
import argparse
import io
import re
import socketserver
import struct
import sys


HEADER = '!HBBHHHH'
HEADER_SIZE = struct.calcsize(HEADER)
DOMAIN_PATTERN = re.compile('^[A-Za-z0-9\-\.\_]+$')

# Data path, will be updated from argparse
data_path = ''


class DNSHandler(socketserver.BaseRequestHandler):

  def handle(self):
    socket = self.request[1]
    data = self.request[0]
    data_stream = io.BytesIO(data)

    # Read header
    (request_id, header_a, header_b, qd_count, an_count, ns_count, ar_count) = struct.unpack(HEADER, data_stream.read(HEADER_SIZE))

    # Read questions
    questions = []
    for i in range(qd_count):
      name_parts = []
      length = struct.unpack('B', data_stream.read(1))[0]
      while length != 0:
        name_parts.append(data_stream.read(length).decode('us-ascii'))
        length = struct.unpack('B', data_stream.read(1))[0]
      name = '.'.join(name_parts)

      if not DOMAIN_PATTERN.match(name):
        print('Invalid domain received: ' + name)
        # Contains invalid characters, don't continue since it may be path traversal hacking
        return

      (qtype, qclass) = struct.unpack('!HH', data_stream.read(4))

      questions.append({'name': name, 'type': qtype, 'class': qclass})

    print('Got request for ' + questions[0]['name'] + ' from ' + str(self.client_address[0]) + ':' + str(self.client_address[1]))

    # Read answers
    try:
      with open(data_path + '/' + questions[0]['name'].lower(), 'r') as f:
        answers = [s.strip() for s in f.read().split("\n") if len(s.strip()) != 0]
    except:
      answers = []

    # Make response (note: we don't actually care about the questions, just return our canned response)
    response = io.BytesIO()

    # Header
    # Response, Authoriative
    response_header = struct.pack(HEADER, request_id, 0b10000100, 0b00000000, qd_count, len(answers), 0, 0)
    response.write(response_header)

    # Questions
    for q in questions:
      # Name
      for part in q['name'].split('.'):
        response.write(struct.pack('B', len(part)))
        response.write(part.encode('us-ascii'))
      response.write(b'\x00')

      # qtype, qclass
      response.write(struct.pack('!HH', q['type'], q['class']))

    # Answers
    for a in answers:
      response.write(b'\xc0\x0c') # Compressed name (pointer to question)
      response.write(struct.pack('!HH', 16, 1)) # type: TXT, class: IN
      response.write(struct.pack('!I', 0)) # TTL: 0
      response.write(struct.pack('!H', len(a) + 1)) # Record length
      response.write(struct.pack('B', len(a))) # TXT length
      response.write(a.encode('us-ascii')) # Text

    # Send response
    socket.sendto(response.getvalue(), self.client_address)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Simple TXT DNS server')
  parser.add_argument('port', metavar='port', type=int,
                      help='port to listen on')
  parser.add_argument('path', metavar='path', type=str,
                      help='path to find results')

  args = parser.parse_args()
  port = args.port
  data_path = args.path

  server = socketserver.ThreadingUDPServer(('', port), DNSHandler)
  print('Running on port %d' % port)

  try:
    server.serve_forever()
  except KeyboardInterrupt:
    server.shutdown()
