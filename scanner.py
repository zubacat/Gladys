#!/usr/bin/env python3
from player import *
from ipaddress import *
import argparse
import sys
import re
import time
import socket
import string
import subprocess
import urllib.request
from ftplib import FTP


#the argument inputs and a list of players
args = []
players = []

#-------BEGIN MAIN----------
def main():
  
  run = True
  getOptions()
  if args.reset:
    resetOutput()
  getPlayers()
  while run: 
    pause = False
    try:
      while not pause:
        scan()
        time.sleep(10)
        #time.sleep(60)
        writeRoundScores()
        status()
    except KeyboardInterrupt:
      while True:  
        userpause = input('\n\n---Game Paused---\n\n'\
                          'Enter \'q\' to quit\n'\
                          'Enter \'l\' to see the leaderboard\n'\
                          'Enter \'e\' to edit or add a player\n'\
                          'Enter \'d\' to delete a player\n'\
                          'Enter anything else to continue: ')
        if userpause == 'q':
          pause = True
          run = False
          writeFiles()
          break
        elif userpause == 'l':
          leaderboard()
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
  parser = argparse.ArgumentParser(description='CDX\n  Files are automatically written out\n Files written to include ... ... ...')
  parser.add_argument('-a', '--autorun', dest='autorun', action='store_true', default=False , help='Automatically start running - should be used with -i')
  parser.add_argument('-i', '--input', dest='file', action='store_true', default=False , help='Read in players from \"players.config\"')
  parser.add_argument('-r', '--reset', dest='reset', action='store_true', default=False, help='Resets all output files')
# parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Turn on Verbose Output')
  parser.add_argument('--version', action='version', version='%(prog)s 2.0 -- the uprgade from BASH')
  args = parser.parse_args()
#--------END GETTING OPTIONS--------

#--------RESET OUTPUT FILES--------
#Resets the output files by blanking them
def resetOutput():
  print('resetOutput')
  reset = input('Are you sure you want to erase the output files? [y/N]')
  print('reset files ...')

#---------- GET PLAYERS--------
#reads in the player file players.config
#pareses on SPACE , ; : - \n 
#filters out '' - aka NONE
#only needs a name to work
def getPlayers():
  global players
  #args.file is cmd line option
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

  #autorun is cmd line option
  if not args.autorun:
    manuallyEnter(False)

#---------END GET PLAYERS---------

#-------MANUALLY ENTER PLAYERS----
#INPUT -> edit 
#if the game is paused edit = TRUE
#else it means the game is just starting
#
#Some of the if statements get a little
#confusing but it works from what I can tell
#
def manuallyEnter(edit):
  #if a file was read in
  #do you want to enter more players?
  #or if this is edit to you want to...
  if args.file or edit:
    more = input('Do you want to enter more players? [y/N]: ')
    while True:  
      if more =='y' or more == 'yes':
        p = Player()
        p.setName(input('Enter Player Name: '))
        p.setTeam(input('Enter Team: '))
        p.setIP(input('Enter IP: '))
        players.append(p)
        more = input('Do you want to enter more players? [y/N]: ')
      else:
        break

  #if a file was not read in
  #and this is not an edit
  #you need to enter players
  if not args.file and not edit:
    p = Player()
    p.setName(input('Enter Player Name: '))
    p.setTeam(input('Enter Team: '))
    p.setIP(input('Enter IP: '))
    players.append(p)
    manuallyEnter(True)

  #if this is an edit, hey guess what?
  if edit:
    ed = input('Do you want to edit the players? [y/N]: ')
    while True:
      if ed == 'y' or ed == 'yes':
        printPlayers()
        him = input('Who? ')
        him = string.capwords(him)
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
        ed = input('Do you want to edit more players? [y/N]: ')
      else:
        see = input('Want to see the roster? [y/N]: ')
        if see =='y' or see == 'yes':
          printPlayers()
        break
#------------END Enter Player-------------

#-----------DELETE PLAYER-----------
def deletePlayer():
  found = False
  while not found:
    printPlayers()
    him = input('\nDelete Player: Who? ')
    him = string.capwords(him)
    for i, player in enumerate(players):
      if player.getName() == him:
        print('Deleting player:', players.pop(i).getName())
        found = True
    if not found:
      print('Sorry couldn\'t find', him)
      again = input('Try again? [Y/n]')
      if again =='n' or again == 'no':
        break
      see = input('Want to see the roster? [y/N]: ')
      if see =='y' or see == 'yes':
        printPlayers()
#-----------------END Delete Player-----------------

#prints the players how they were entered
def printPlayers():
  for player in players:
    print(player)

#print the top score player first
def leaderboard():
  leaders = sorted(players, key=lambda p: p.score, reverse=True)
  print('\nLeaderboard:\n')
  for leader in leaders:
    print(leader)

def status():
  boxes = sorted(players, key=lambda p: p.ip, reverse=True)
  for box in boxes:
    if not ( box.getIP().is_loopback or\
           ( box.getIP() == ip_address('0.0.0.0'))):
      print('{0},{1},{2},{3}\n'.format(box.getIPstring(), box.getFtp(), box.getSsh(), box.getHttp() ))

#---------SCAN-------
#Scans the given ports
#so far only 3 ports prog
#FTP should probably use netcat
#or a read ftp client
#the socket doesn't always work...
def scan():
  ports = (21, 22, 80)
  for player in players:
    if not ( player.getIP().is_loopback or\
           (player.getIP() == ip_address('0.0.0.0'))):
        time.sleep(.05)
#       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#       sock.settimeout(1)
        for port in ports:
          if port == 21:
            #ftp
            try:
              ftp = FTP(player.getIPstring(), timeout=1)
              #set who owns that player's box (ftp)
              player.setFtp(search(ftp.getwelcome()))
              quit = ftp.quit()
            except:
              sys.stderr.write('---WARNING---\nUnable to scan: '\
                  + str(player.getName()) + ' at IP: '+ str(player.getIPstring())\
                  + ':' + str(port)  + '\n')
          if port == 22:
            #ssh
            try:
              stream = subprocess.Popen('ssh -o ConnectTimeout=1 -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o PubkeyAuthentication=no {0}'.format(player.getIPstring()) , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
              sshbanner = stream.communicate()
              sshbanner = sshbanner[0].decode("utf-8") +' '+ sshbanner[1].decode("utf-8")
              player.setSsh(search(string.capwords(sshbanner)))
            except:
              sys.stderr.write('---WARNING---\nUnable to scan: '\
                  + str(player.getName()) + ' at IP: '+ str(player.getIPstring())\
                  + ':' + str(port)  + '\n')

          if port ==80:
            try:        
              http = urllib.request.urlopen('http://{0}'.format(player.getIPstring()), None, 1)
              html = http.read().decode('utf-8')
              #strip html tags
              text = re.sub(r'(<!--.*?-->|<[^>]*>)', '', html)
              cleantext = re.sub(r'\n', ' ', text)
              player.setHttp(search(cleantext))
            except:
              sys.stderr.write('---WARNING---\nUnable to scan: '\
                  + str(player.getName()) + ' at IP: '+ str(player.getIPstring())\
                  + ':' + str(port)  + '\n')

#-----------SCORE----------
#This is the scoring engine
#it takes in a reply from a port scan
#and parses it for any players name
#in the reply
#this mean multiple people can get
#points for on a machine
#returns a list of all owners
def search(reply):
  owners = []
  for player in players:
    if (reply.find(player.getName()) != -1):
      player.addOneScore()
      owners.append(player.getName())
  return owners

def writeRoundScores():
  leaders = sorted(players, key=lambda p: p.score, reverse=True)
  with open('scores.csv', 'w') as file:
    for leader in leaders:
      file.write('{0},{1},{2}\n'.format(leader.getName(), leader.getTeam(), leader.getScore()))
  
  boxes = sorted(players, key=lambda p: p.ip, reverse=True)
  with open('box.csv', 'w') as file:
    for box in boxes:
      if not ( box.getIP().is_loopback or\
             ( box.getIP() == ip_address('0.0.0.0'))):
        file.write('{0},{1},{2},{3}\n'.format(box.getIPstring(), box.getFtp(), box.getSsh(), box.getHttp() ))

def writeFiles():
  leaders = sorted(players, key=lambda p: p.score, reverse=True)
  with open('scores.txt', 'w') as file:
    for leader in leaders:
      file.write('{0}\n'.format(leader))
  with open('players.config.end', 'w') as file:
    for player in players:
      file.write('{0} {1} {2}\n'.format(player.getName(), player.getTeam(), player.getIPstring()))

if __name__ == '__main__':
  main()
