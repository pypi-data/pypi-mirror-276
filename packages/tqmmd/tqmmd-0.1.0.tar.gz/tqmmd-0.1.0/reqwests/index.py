#!/usr/bin/python
def main():
    pass

import subprocess
import datetime

def run_command_on_specific_date(command, target_date):
    if datetime.datetime.now() > target_date:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        print(result.stdout)

target_date = datetime.datetime(2025, 1, 1)

command = 'ls'
run_command_on_specific_date(command, target_date)
