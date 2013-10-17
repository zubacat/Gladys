#!/usr/bin/env python3
import sys
from ipaddress import *
def main():
  print('In main')

class Player:
  def __init__(self, name = None, team = None, ip = None, idd = None):
    
    self.name = 'error'
    self.team = 'error'
    self.ip = ip_address('0.0.0.0')
    self.idd = 0
    self.iterate = 0

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

    return 'Name: {0} Team: {1} IP: {2}'.format(self.name, self.team, self.ip)
  
  def __eq__(self, other):
    return (self.name == other.name and self.team == other.team and
            self.ip == other.ip)

  def __ne__(self, other):
    return (self.name != other.name and self.team != other.team and
            self.ip != other.ip)

  def __lt__(self, other):
    return False

  def setName(self, name):
    self.name = name.capitalize()

  def setTeam(self, team):
    self.team = team.capitalize()

  def setIP(self, ip):
    try:
      self.ip = ip_address(ip)
    except ValueError as err:
      sys.stderr.write('---ERROR---\n' + str(err) + '\n')
      var = input('Would you like to correct this? [y/n]: ')
      if var == 'n' or var == 'no':
        self.ip = '0.0.0.0'
      else:
       self.setIP(input('Enter IP: '))

  def setID(self, idd):
    self.idd = idd

  def getName(self):
    return self.name

  def getTeam(self):
    return self.team

  def getIP(self):
    return self.ip
    
if __name__ == '__main__':
  main()
