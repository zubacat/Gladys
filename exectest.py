#!/usr/bin/env python3
import subprocess as sub
def main():
  print('in main')

  ip = '192.168.1.75'
  s = sub.Popen('ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o PubkeyAuthentication=no user@%s'%ip , shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
# s = sub.Popen('ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no -o PubkeyAuthentication=no user@192.168.1.75', shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

# s = sub.Popen(['ls','-a', '-o'], stdout=sub.PIPE, stderr=sub.PIPE)
  print(s)
  thelist = s.communicate()
  print(thelist)
  print(thelist[1])
  print(thelist[1].decode("utf-8"))
  li = thelist[1].decode("utf-8")
  print(li)

# print(s.stdout.read())
# print(s.stderr.read())

if __name__ == '__main__':
  main()

