#!/usr/bin/env python3
import paramiko
def main():
  print('in main')
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('192.168.1.75', username='user', password='password')
  ssh.connect('192.168.1.93', username='user', password='password')
  stdin, stdout, stderr = ssh.exec_command("ls")
  print(stdout.readlines())


if __name__ == '__main__':
  main()

