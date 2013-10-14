#!/usr/bin/env python3
from player import *
from ipaddress import *
import argparse
import sys
import re

args = []

def main():
  
  run = True
  getOptions()
  while run: 
    getPlayers()
    pause = False
    while not pause:
      go()

def getOptions():
  global args
  parser = argparse.ArgumentParser(description='Option Getter module for CDX\n Files are automatically written out\n Files written to include ... ... ...')
  parser.add_argument('-i', '--input', dest='file', action='store_true', default=False , help='Read in players from \"players.config\"')
  parser.add_argument('-r', '--reset', dest='reset', action='store_true', default=False, help='Resets all output files')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Turn on Verbose Output')
  parser.add_argument('--version', action='version', version='%(prog)s 2.0 -- the uprgade from BASH')
  args = parser.parse_args()

def getPlayers():
  
    
  
  

if __name__ == '__main__':
  main()
