#!/usr/bin/env python3
from player import *
from ipaddress import *
import argparse
import sys
import re
import time

args = []
players = []

#-------BEGIN MAIN----------
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
      while True:  
        userpause = input('\n\n---Game Paused---\n\n'\
                          'Enter \'s\' to stop\n'\
                          'Enter \'l\' to see the leaderboard\n'\
                          'Enter \'e\' to edit or add a player\n'\
                          'Enter \'d\' to delete a player\n'\
                          'Enter anything else to continue: ')
        if userpause == 's':
          pause = True
          run = False
          print('finishing writing files')
          break
        elif userpause == 'l':
          print('show leaderboard')
        elif userpause == 'e':
          manuallyEnter(True)
        elif userpause == 'd':
          deletePlayer()
        else:
          print('\n---Game Resumed---\n\n')
          break
 
#-----------END MAIN------------------


#---------BEGIN GETTING OPTIONS-------
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
    while True:  
      if more =='y' or more == 'yes':
        p = Player()
        p.setName(input('Enter Player Name: '))
        p.setTeam(input('Enter Team: '))
        p.setIP(input('Enter IP: '))
        players.append(p)
        more = input('Do you want to enter more players? [y/n]: ')
      else:
        break
  
  if not args.file and not edit:
    p = Player()
    p.setName(input('Enter Player Name: '))
    p.setTeam(input('Enter Team: '))
    p.setIP(input('Enter IP: '))
    players.append(p)
    manuallyEnter(True)

  if edit:
    ed = input('Do you want to edit the players? [y/n]: ')
    while True:
      if ed == 'y' or ed == 'yes':
        printPlayers()
        him = input('Who? ')
        him = him.capitalize()
        found = False
        for player in players:
          if player.getName() == him:
            print('Editing player: ', player.getName())
            player.setName(input('Enter New Player Name: '))
            player.setTeam(input('Enter New Team: '))
            player.setIP(input('Enter New IP: '))
            found = True
        if not found:
          print('Sorry couldn\'t find', him)
        ed = input('Do you want to edit more players? [y/n]: ')
      else:
        see = input('Want to see the roster? [y/n]: ')
        if see =='y' or see == 'yes':
          printPlayers()
        break
#--------------------END Enter Player-------------------


def deletePlayer():
  found = False
  while not found:
    printPlayers()
    him = input('\nDelete Player: Who? ')
    him = him.capitalize()
    for i, player in enumerate(players):
      if player.getName() == him:
        print('Deleting player:', players.pop(i).getName())
        found = True
    if not found:
      print('Sorry couldn\'t find', him)
      again = input('Try again? [y/n]')
      if again =='n' or again == 'no':
        break
      see = input('Want to see the roster? [y/n]: ')
      if see =='y' or see == 'yes':
        printPlayers()
#-----------------END Delete Player-----------------

def printPlayers():
  for player in players:
    print(player)

def go():
  print('go')
 

if __name__ == '__main__':
  main()
