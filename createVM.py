#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

def welcome_print(msg):
    print('*' * 70)
    print('   <<< ' + msg + ' >>>')
    print('*' * 70)

welcome_print('Create your KVM virtual machine, powered by blueyi')

# command to run and get the output
def run_cmd_reout(cmd, args=' ', con = False):
    tcall_cmd = cmd + ' ' + args
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
    touput = p.communicate()[0]
    if p.returncode != 0 :
        print('<<< ' + tcall_cmd + ' >>> run failed!')
        if not con :
            sys.exit(1)
    print(toutput)
    return toutput

# path
# script path
curr_path = os.path.split(os.path.realpath(__file__))[0]
# user path
user_path = os.path.expanduser('~')

# list all kvm exist
print('All virtual machine list in the following')
run_cmd_reout('virsh list --all')

hostname = input("Enter your unique hostname(必须为英文，且以自己的姓名简拼开头，例如wyl-Master):")
template_kvm = 'ubuntuServer1604-original'
image_path = '/home/vm/'

# clone kvm
clone_cmd = 'virt-clone --original=' + template_kvm  + ' --name=' + hostname + ' --file=' + image_path + hostname + '.qcow2'
run_cmd_reout(clone_cmd)

# sysprep kvm
sysprep_cmd = 'virt-sysprep -d ' + hostname + ' --hostname ' + hostname
run_cmd_reout(sysprep_cmd)

# start hostname vm
start_vm_cmd = 'virsh start ' + hostname
run_cmd_reout(start_vm_cmd)

# get uuid, mac, cpu core, ram, disk of cloned domain
host_dumpxml_cmd = 'virsh dumpxml ' + hostname
hostDumpxml = run_cmd_reout(host_dumpxml_cmd)
hostMac = ''
hostCpuCore = 0
hostRam = 0
hostDisk = 0
hostArch = ''





