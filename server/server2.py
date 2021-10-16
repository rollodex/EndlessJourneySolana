#!/usr/bin/env python3
"""
Passthrough server for dialog continuation
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import openai
import json

openai.api_key = "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"

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        logging.info("POST request,\n\rPath: %s\n\rHeaders:\n\r%s\n\r", str(self.path), str(self.headers))
        #self._set_response()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        text = post_data.decode('utf-8')
        data = json.loads(text)

        response = openai.Completion.create(
            engine="davinci",
            prompt=data["text"],
            temperature=0.66,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.18,
            presence_penalty=0.32
          )

        self._set_response()
        self.wfile.write(response.choices[0].text.encode()) #.format(self.path).encode('utf-8'))
        logging.info(response.choices[0].text.encode())

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()





def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
