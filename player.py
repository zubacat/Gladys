#!/usr/bin/env python3
import sys
import string
from ipaddress import *
def main():
  print('In main, shouldnt be here')

class Player:
  def __init__(self, name = None, team = None, ip = None):
    
    self.name = 'error'
    self.team = 'error'
    self.ip = ip_address('0.0.0.0')
    self.score = [0]
    self.iterate = 0
    #ftp,ssh,http are the names of the owners of the players box
    self.ftp = [] 
    self.ssh = []
    self.http = []

  def __iter__(self):
    return self

  def next(self):
    if self.iterate == 0:
      self.iterate += 1
      return self.name
    if self.iterate == 1:
      self.iterate += 1
      return self.team
    if self.iterate == 2:
      self.iterate += 1
      return self.ip
    if self.iterate ==3:
      self.iterate = 0
      raise StopIteration

  def __str__(self):
    return 'Name: {0} Team: {1} IP: {2} Score: {3}'.format(self.name, self.team, self.ip, self.score[0])
  
  def __eq__(self, other):
    return (self.name == other.name and self.team == other.team and
            self.ip == other.ip)

  def __ne__(self, other):
    return (self.name != other.name and self.team != other.team and
            self.ip != other.ip)

  def setName(self, name):
    self.name = string.capwords(name)

  def setTeam(self, team):
    self.team = string.capwords(team)

  def setFtp(self, ftp):
    self.ftp = ftp
 
  def setSsh(self, ssh):
    self.ssh = ssh
  
  def setHttp(self, http):
    self.http = http

  def setIP(self, ip):
    try:
      self.ip = ip_address(ip)
    except ValueError as err:
      sys.stderr.write('---ERROR---\n' + str(err) + '\n')
      var = input('Would you like to correct this? [Y/n]: ')
      if var == 'n' or var == 'no':
        self.ip = ip_address('0.0.0.0') 
      else:
       self.setIP(input('Enter IP: '))

  def addOneScore(self):
    self.score.insert(0, self.score[0] + 1)

  def setScore(self, score):
    self.score.insert(0, score)

  def resetScore(self):
    self.score = [0]

  def getName(self):
    return self.name

  def getTeam(self):
    return self.team

  def getFtp(self):
    return self.ftp

  def getSsh(self):
    return self.ssh

  def getHttp(self):
    return self.http

  def getIP(self):
    return self.ip
  
  def getIPstring(self):
    return '{0}'.format(self.ip)

  def getScore(self):
    return self.score[0]

  def getScores(self):
    return self.score

if __name__ == '__main__':
  main()
