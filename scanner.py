#!/usr/bin/env python3
from player import *
from ipaddress import *
import argparse
import sys
import re
import time

args = []
players = []


def main():
  
  run = True
  getOptions()
  if args.reset:
    resetOutput()
  getPlayers()
  if args.verbose:
    printPlayers()
  while run: 
    pause = False
    try:
      while not pause:
        go()
        time.sleep(3)
        #time.sleep(60)
    except KeyboardInterrupt:
      userpause = input('\n---Game Paused---\n'\
                        'Press \'s\' to stop\n'\
                        'Press \'e\' to edit or add a player\n'\
                        'Press \'d\' to delete a player\n'\
                        'Press anything else to continue: ')
      if userpause == 's':
        pause = True
        run = False
        print('finishing writing files')
      elif userpause =='e':
        manuallyEnter(True)
      elif userpause == 'd':
        #deletePlayer()
        print('deleteplayer')
      else:
        print('---Game Resumed---')
 
#-----------END MAIN------------------

def getOptions():
  global args
  parser = argparse.ArgumentParser(description='Option Getter module for CDX\n Files are automatically written out\n Files written to include ... ... ...')
  parser.add_argument('-a', '--autorun', dest='autorun', action='store_true', default=False , help='Automatically start running - should be used with -i')
  parser.add_argument('-i', '--input', dest='file', action='store_true', default=False , help='Read in players from \"players.config\"')
  parser.add_argument('-r', '--reset', dest='reset', action='store_true', default=False, help='Resets all output files')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Turn on Verbose Output')
  parser.add_argument('--version', action='version', version='%(prog)s 2.0 -- the uprgade from BASH')
  args = parser.parse_args()

def resetOutput():
  print('resetOutput')
  reset = input('Are you sure you want to erase the output files? [y/n]')
  print('reset files ...')

def getPlayers():
  global players
  if args.file:
    try:
      with open('players.config', 'r') as f:
        for line in f:
          if line[0] == '#':
            continue
          p = Player()
          parsed = re.split(' |,|;|:|-|\n', line)
          parsed =  list(filter(None, parsed))
          p.setName(parsed.pop(0))
          try:
            p.setTeam(parsed.pop(0))
          
          except IndexError as err:
          #only name arguments given no team -- assume whitecell
            p.team = 'white'
            sys.stderr.write('---WARNING---\nNo Team given for Player: '
                             + str(p.name) + '\nSetting to White\n')
          try:
            p.setIP(parsed.pop(0))
          except IndexError as err:
          #only name arguments given no IP -- assume 0.0.0.0
            p.setIP('0.0.0.0')
            sys.stderr.write('---WARNING---\nNo IP given for Player: '
                            + str(p.name) + '\nSetting to 0.0.0.0\n')
          players.append(p)
    except FileNotFoundError as readerr:
      sys.stderr.write('File Not Found\n' + str(readerr) + '\n')

  if not args.autorun:
    manuallyEnter(False)

#---END read in file---

def manuallyEnter(edit):
  if args.file or edit:
    more = input('Do you want to enter more players? [y/n]: ')
    if more =='y' or more == 'yes':
      p = Player()
      p.setName(input('Enter Player Name: '))
      p.setTeam(input('Enter Team: '))
      p.setIP(input('Enter IP: '))
      players.append(p)
  
  if not args.file and not edit:
    p = Player()
    p.setName(input('Enter Player Name: '))
    p.setTeam(input('Enter Team: '))
    p.setIP(input('Enter IP: '))
    players.append(p)

  if edit:
    ed = input('Do you want to edit the players? [y/n]: ')
    if ed == 'y' or ed == 'yes':
      printPlayers()
      him = input('Who? ')
      him = him.capitalize()
      for player in players:
        print('Player',player.getName())
        print('Him',him)
        if player.getName() == him:
          player.setName(input('Enter Player Name: '))
          player.setTeam(input('Enter Team: '))
          player.setIP(input('Enter IP: '))
        else:
          print('Sorry couldn\'t find', him)
          

  see = input('Want to see the roster? [y/n]: ')
  if see =='y' or see == 'yes':
    printPlayers()

def printPlayers():
  for player in players:
    print(player)

def go():
  print('go')
 

if __name__ == '__main__':
  main()
