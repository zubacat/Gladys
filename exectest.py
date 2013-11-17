#!/usr/bin/env python3
import subprocess
def main():
  print('in main')
# stream = subprocess.Popen(['ssh', ' -oStrictHostKeyChecking=no', ' -o PasswordAuthentication=no', ' -o PubkeyAuthentication=no', ' user@192.168.1.93'], shell=True)

  stream = subprocess.Popen('ssh -oStrictHostKeyChecking=no -o PasswordAuthentication=no -o PubkeyAuthentication=no user@192.168.1.93', shell=True, stdout=subprocess.PIPE)

if __name__ == '__main__':
  main()

