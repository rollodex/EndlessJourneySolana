#!/usr/bin/env python3

#make_token.py - make a solana token as NFT, mint 1, and transfer to a recipient (sender pays)
#it mints semi-fungible tokens (since each badge is keyed by name, so if players get the same acheivement, it will become less rare
#this script will add the name and address to the pickledb token registry
#it returns as output the address of the newly created NFT

import sys
import os
import pickledb

name = sys.argv[1]
recipient = sys.argv[2]
db = pickledb.load('./registry.db', False)

if db.get(name) == False:
   token_creation = os.popen('spl-token create-token --decimals 0')
   addr_output = token_creation.read()

   token_addr = addr_output[15:59]

   account_creation = os.popen('spl-token create-account ' + token_addr)
   acc_output = account_creation.read()

   acc_addr = acc_output[17:61]

   token_mint = os.popen('spl-token mint ' + token_addr +' 1 ' + acc_addr) 
   mint_result = acc_output = token_mint.read()

   token_transfer = os.popen('spl-token transfer --fund-recipient --allow-unfunded-recipient ' + token_addr + ' 1 ' + recipient)
   transfer_result = token_transfer.read()

   print(token_addr)
   db.set(name,token_addr + ',' + acc_addr)
   db.dump()

else:
   account_addresses = db.get(name).split(',')
   token_addr = account_addresses[0]
   acc_addr = account_addresses[1]
   token_mint = os.popen('spl-token mint ' + token_addr +' 1 ' + acc_addr) 
   mint_result = acc_output = token_mint.read()

   token_transfer = os.popen('spl-token transfer --fund-recipient --allow-unfunded-recipient ' + token_addr + ' 1 ' + recipient)
   transfer_result = token_transfer.read()

   print(token_addr)
   
