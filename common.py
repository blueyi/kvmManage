#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 blueyi <blueyi@blueyi-ubuntu>
#
# Distributed under terms of the MIT license.

import subprocess
import sys

"""
Some function and const value
"""

image_path = '/home/blueyi/vhost/image/'
iso_path = 'home/blueyi/vhost/iso/'


# print some important string
def welcome_print(msg):
    print('*' * 70)
    print('   <<< ' + msg + ' >>>')
    print('*' * 70)

# run an shell command in subprocess
def run_cmd_reout(tcall_cmd, goOnRun = False, isOutPut = True, jumpErr = False, isRetuenCode = False):
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
    toutput = p.communicate()[0]
    if p.returncode != 0 and not jumpErr:
        print('<<< ' + tcall_cmd + ' >>> run failed!')
        if not goOnRun :
            sys.exit(1)
    if isOutPut :
        print(toutput)
    if isRetuenCode :
        return p.returncode
    else :
        return toutput

# Is specified KVM running
def isVMRunning(host_name) :
    is_run_cmd = 'virsh domstate ' + host_name
    return (run_cmd_reout(is_run_cmd, goOnRun=True, isOutPut=False, jumpErr=True, isRetuenCode=True) == 0) and (run_cmd_reout(is_run_cmd, goOnRun=True, isOutPut=False, jumpErr=True).strip() == 'running')

# list all kvm exist
def listAllKVM() :
    print('All virtual machine list in the following')
    run_cmd_reout('virsh list --all')

# Get VNC port
def getVNCPort(host_name) :
    vnc_display_cmd = 'virsh vncdisplay ' + host_name
    vnc_reout = run_cmd_reout(vnc_display_cmd, isOutPut=False)



