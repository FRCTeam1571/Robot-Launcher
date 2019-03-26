#!/usr/bin/env python3

import os
import platform
import argparse
import sys
import configparser

parser = argparse.ArgumentParser()
parser.add_argument('robot', nargs="?", help="How to upload to the robot, optional unless changing modes (Radio or USB)")
parser.add_argument('-S','--sim', help="Run in Simulator instead of deploying", action="store_true")
parser.add_argument('-s', '--skiptests', help="Skip Tests", action='store_true')
parser.add_argument('-i', '--init', help="Initalize robot radio IP Address", action='store_true')


# Allows you to call arguments using args.[argument]
args = parser.parse_args()


def run():
    python = sys.executable
    cwd = os.getcwd()
    robotFile = cwd + "/robot.py"
    robot = str(args.robot).lower()
    config = configparser.ConfigParser()

    config.read(cwd + "/.deploy_cfg")

    if not "ip address" in config or args.init:
        print("Initalizing, Please input Radio IP Address, *not* USB Address (10.XX.XX.1)")
        radioIP = input(": ")
        config['ip address'] = {
            'radio': radioIP,
            'usb': '172.22.11.2'
        }

        with open(cwd + "/.deploy_cfg", 'w') as configfile:
            config.write(configfile)
            configfile.close()

        print("Radio IP Address set as: " + config["ip address"]['radio'] + ".\nPlease run again as 'launch usb' or 'launch radio'")

        
        sys.exit()





    if args.sim:
        depsim = "sim"
    else:
        depsim = "deploy"
    
    if robot != "none":

        if robot == "usb":
            ipAddress = config["ip address"]["usb"]
        elif robot == "radio":
            ipAddress = config["ip address"]["radio"]
        else:
            ipAddress = robot



        config['auth'] = {
            'hostname': ipAddress
        }
        
        with open(cwd + "/.deploy_cfg", 'w') as configfile:
            config.write(configfile)
            configfile.close()

    if args.skiptests:
        skip = "--skip-tests"
    else:
        skip = ""
    
    print("Starting...")
    os.system(python + " " + robotFile + " " + depsim + " " + skip)
