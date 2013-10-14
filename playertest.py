#!/usr/bin/env python3
from player import *
from ipaddress import *
import sys
import re

def main():

  players = []
  try:
    with open('players.config', 'r') as f:
      for line in f:
  #     print(line, end='')
        if line[0] == '#':
          continue
        p = Player()
        parsed = re.split(' |,|;|:|-|\n', line)
        parsed =  list(filter(None, parsed))
        p.setName(parsed.pop(0).capitalize())
        try:
          p.setTeam(parsed.pop(0).capitalize())
        
        except IndexError as err:
        #only name arguments given no team -- assume whitecell
          p.team = 'white'.capitalize()
          sys.stderr.write('---WARNING---\nNo Team given for Player: '
                           + str(p.name) + '\nSetting to White\n')
        try:
          p.setIP(parsed.pop(0))
        except IndexError as err:
        #only name arguments given no team -- assume whitecell
          p.setIP('0.0.0.0')
          sys.stderr.write('---WARNING---\nNo IP given for Player: '
                          + str(p.name) + '\nSetting to 0.0.0.0\n')
        players.append(p)
    for text in players:
      print(text)
  except FileNotFoundError as readerr:
    sys.stderr.write('File Not Found\n' + str(readerr) + '\n')

if __name__ == '__main__':
  main()
