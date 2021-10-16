#!/usr/bin/env python3
"""
Send a prompt encoded in JSON to the game server
Usage::
    ./server.py <OpenAI Key>
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
import openai
import json
import pickledb

openai.api_key = sys.argv[1]
db = pickledb.load('./registry.db', False)
hardcode_transfer_addr = '7TJsMfXspguH52xEEZyvjvytB8NzmB5E29tWyPqvBugi'

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_PUT(self):
        logging.info("PUT request,\n\rPath: %s\n\rHeaders:\n\r%s\n\r", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("PUT request for {}".format(self.path).encode('utf-8'))
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        response = openai.Completion.create(
            engine="davinci",
            prompt=post_data,
            temperature=0.66,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.18,
            presence_penalty=0.32
          )

        self._set_response()
        self.wfile.write(response.choices[0].text.encode()) #.format(self.path).encode('utf-8'))
        logging.info(response.choices[0].text.encode())


    def do_POST(self):
       if self.path == '/':
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        the_json = post_data.decode('utf-8')
        the_dict =  json.loads(the_json)
        solana_wallet = the_dict["wallet"]
        logging.info('wallet: ' + solana_wallet)
        
        header= "AI Bandersnatch Choose Your Own Adventure Game\n\n------------\n\n"
        pretext = "Date:7/1\nBranch:In this world, you can be who you want to be. All you must do is awaken and enter your truest desires. Let the games begin! \nEmotion: optimistic | Adjectives: exicted, fascinated | Energy: 100% | Water: 100% | Integrity: 100% | Affiliation: 100% | Certainity: 100% | Competence: 100%\nAchievement: Trepid Adventurer\nBranch A: Start the adventure! | Branch B: Stay in bed.\n> You choose Branch A.\n------------\n\n"
        branch_header = "Date:7/2\nBranch:"
        stats_bar = "Emotion: " + the_dict["init_emotion"] + " | Adjectives: " + the_dict["adj_one"] + ", " + the_dict["adj_two"] + " | Energy: " + the_dict["init_energy"] + " | Water: " + the_dict["init_water"] + " | Integrity: " + the_dict["init_integrity"] + " | Affiliation: " + the_dict["init_affiliation"] +" | Certainty: " + the_dict["init_certainty"] + " | Competence: " + the_dict["init_competence"] + "\n"
        branches = "Branch A: " + the_dict["branch_a"] + " | " + "Branch B: " + the_dict["branch_b"] + "\n"
        branch_choice = the_dict["init_choice"]
        branch_prompt = "> You chose branch "
        restart_sequence = "\n------------\n"



        prompt = header + pretext + branch_header + the_dict["story"] + "\n" + stats_bar + "\n" + "Achievement: " + the_dict["init_ach"] + "\n" + branches + "\n" + branch_prompt + branch_choice + restart_sequence
        logging.info(prompt)


        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.66,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.18,
            presence_penalty=0.32
          )

        self._set_response()
        self.wfile.write(response.choices[0].text.encode()) #.format(self.path).encode('utf-8'))
        #if response has an acheivement, call make-token script
        lines = response.choices[0].text.split("\n")
        res = [i for i in lines if i.startswith("Achievement: ")]
        if(len(res) > 0):
           the_achievement = res[0][13:];
           logging.info("Achievement: " + the_achievement)
           result = os.popen('./make_token.py ' + '"' + the_achievement + '" ' + solana_wallet)
           token_addr = result.read()
        
        #logging.info(response.choices[0].text.encode())
       elif self.path == '/continue':
        logging.info("POST request,\n\rPath: %s\n\rHeaders:\n\r%s\n\r", str(self.path), str(self.headers))
        #self._set_response()

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        text = post_data.decode('utf-8')
        data = json.loads(text)
        solana_wallet = data["wallet"]
        logging.info('wallet: ' + solana_wallet)

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
        #if output has an acheivement, log name and token to key/value store:
        lines = response.choices[0].text.split("\n")
        res = [i for i in lines if i.startswith("Achievement: ")]
        if (len(res) > 0):
           the_achievement = res[0][13:];
           logging.info("Achievement: " + the_achievement)
           result = os.popen('./make_token.py ' + '"' + the_achievement + '" ' + solana_wallet)
           token_addr = result.read()
        elif self.path == '/addr':
          logging.info("POST request,\n\rPath: %s\n\rHeaders:\n\r%s\n\r", str(self.path), str(self.headers))
          content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
          post_data = self.rfile.read(content_length) # <--- Gets the data itself
          text = post_data.decode('utf-8')
          data = json.loads(text)
          token_address = db.get(data["name"])
          self._set_response()
          self.wfile.write(token_address) #.format(self.path).encode('utf-8'))    
        return

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
   run()
