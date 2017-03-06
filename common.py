#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 blueyi <blueyi@blueyi-ubuntu>
#
# Distributed under terms of the MIT license.

import subprocess
import sys
import time

"""
Some function and const value
"""

image_path = '/mnt/data/vhost/image/'
iso_path = '/mnt/data/vhost/iso/'
template_kvm = 'ubuntuServer1604-original'
sub_ip = '192.168.1.0'
addDisk_path = '/mnt/data/addDisk/'


itoa = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

# print some important string
def welcome_print(msg):
    print('*' * 70)
    print('   <<< ' + msg + ' >>>')
    print('*' * 70)

# run an shell command in subprocess
def run_cmd_reout(tcall_cmd, goOnRun = False, isOutPut = True, jumpErr = False, isReturnCode = False):
    p = subprocess.Popen(tcall_cmd, shell=True, stdout=subprocess.PIPE, executable='/bin/bash')
    toutput = p.communicate()[0]
    if p.returncode != 0 and not jumpErr:
        print('<<< ' + tcall_cmd + ' >>> run failed!')
        if not goOnRun :
            sys.exit(1)
    if isOutPut :
        print(toutput)
    if isReturnCode :
        return p.returncode
    else :
        return toutput


# get total domain name list
def hostNameList():
    list_cmd = 'virsh list --all'
    list_out = run_cmd_reout(list_cmd, goOnRun=True, isOutPut=False, jumpErr=True, isReturnCode=False)
    host_list = []
    cont = 2
    for line in list_out.strip().split('\n'):
        if cont > 0:
            cont = cont - 1
            continue
        host = line.split()[1]
        host_list.append(host)
    return host_list

# Is specified KVM exist
def isVMExist(host_name) :
    return (host_name in hostNameList())

# Is specified KVM running
def isVMRunning(host_name) :
    is_run_cmd = 'virsh domstate ' + host_name
    return isVMExist(host_name) and (run_cmd_reout(is_run_cmd, goOnRun=True, isOutPut=False, jumpErr=True).strip() == 'running')

# list all kvm exist
def listAllKVM() :
    print('All virtual machine list in the following')
    run_cmd_reout('virsh list --all')

# create disk
def createDisk(path, size) :
    create_disk_cmd = 'qemu-img create -f qcow2 ' + path + ' ' + str(size) + 'G'
    run_cmd_reout(create_disk_cmd)

# get image detail info
def imgDetailInfo(path) :
    img_info_cmd = 'sudo qemu-img info ' + path
    run_cmd_reout(img_info_cmd)

# get image info
def imgInfo(path) :
    img_info_cmd = 'ls -sh ' + path
    run_cmd_reout(img_info_cmd)

# attach disk to vm
def addDisk(host_name, size) :
    tistr = time.strftime('%Y%m%d%H%M%S')
    disk_path = addDisk_path + host_name + '-' + str(tistr) + '.qcow2'
    createDisk(disk_path , size)
    adddisk_cmd = 'virsh attach-disk ' + host_name + ' --source ' + disk_path + ' --target vd' + itoa[int(tistr) % 10] + ' --subdriver qcow2 --targetbus virtio --persistent'
    run_cmd_reout(adddisk_cmd)

# Get disk list of kvm
def getDiskList(host_name) :
    disk_list_cmd = 'virsh domblklist ' + host_name
    output = run_cmd_reout(disk_list_cmd, jumpErr=True, goOnRun=True)
    tlist = output.split()
    disk_list = []
    for line in tlist :
        if '/' in line and ('.qcow2' in line or '.img' in line) :
            disk_list.append(line)
    return disk_list

# Get disk info of kvm
def getDiskInfo(host_name, detail = False) :
    for disk in getDiskList(host_name) :
        if detail :
            imgDetailInfo(disk)
        else :
            imgInfo(disk)

# Get VNC port
def getVNCPort(host_name) :
    if not isVMRunning(host_name) :
        return host_name + ' Not Running!'
    vnc_display_cmd = 'virsh vncdisplay ' + host_name
    vnc_reout = run_cmd_reout(vnc_display_cmd, goOnRun=True, isOutPut=False, jumpErr=True)
    vnc_port = 5900 + int(vnc_reout[(vnc_reout.find(':') + 1) : ])
    return str(vnc_port)

# Get MAC address
def getMAC(host_name) :
    if not isVMExist(host_name) :
        return host_name + ' Not Exist!'
    get_mac_cmd = "virsh dumpxml " + host_name + " | grep 'mac address' | cut -c 21-37"
    return run_cmd_reout(get_mac_cmd, goOnRun=True, isOutPut=False).strip()

# Get ip address
def getIP(host_name, wait=20) :
    if not isVMRunning(host_name) :
        return host_name + ' Not Running!'
    host_mac = getMAC(host_name)

    arp_ip = ''
    start_time = int(time.time())
    # wait for kvm start finish
    while (arp_ip == '' and int(time.time()) - start_time < wait):
        nmap_cmd = 'nmap -sP --host-timeout 15s ' + sub_ip + '/24'
        run_cmd_reout(nmap_cmd, goOnRun=True, isOutPut=False)
        arp_ip_cmd = "arp -an | grep '"  + host_mac + "'"
        arp_ip = run_cmd_reout(arp_ip_cmd, goOnRun=True, isOutPut=False, jumpErr=True)
    if len(arp_ip) == 0 :
        return 'Get ' + host_name + ' ip address failed! MAC:' + host_mac
    else :
        return arp_ip[arp_ip.find('(') + 1 : arp_ip.find(')')]

# get specified KVM info, mac, ip and vnc port
def getVMInfo(host_name, isdetail=False, wait=20) :
    if not isVMExist(host_name) :
        print('<<< ' + host_name + ' Not Exist! >>>')
        return
    print('------' + host_name + ' infomation------')
    host_info_cmd = 'virsh dominfo ' + host_name
    run_cmd_reout(host_info_cmd)
    getDiskInfo(host_name, isdetail)
    print('MAC address: \n' + getMAC(host_name))
    welcome_print(host_name + ' IP: ' + getIP(host_name, wait) + ', VNC port: ' + getVNCPort(host_name) +  ' enjoy it!')


# Start kvm
def startVM(host_name) :
    if not isVMExist(host_name) :
        print('<<< ' + host_name + ' Not Exist! >>>')
        listAllKVM()
        return
    if isVMRunning(host_name) :
        print('<<< ' + host_name + ' has Running! >>>')
        listAllKVM()
        return
    start_cmd = 'virsh start ' + host_name
    run_cmd_reout(start_cmd)
    getVMInfo(host_name)

# Shutdown kvm
def shutdownVM(host_name, isforce=False) :
    if not isVMExist(host_name) :
        print('<<< ' + host_name + ' Not Exist! >>>')
        listAllKVM()
        return
    if not isVMRunning(host_name) :
        print('<<< ' + host_name + ' Not Running! >>>')
        listAllKVM()
        return
    shutdown_cmd = ''
    if isforce :
        shutdown_cmd = 'virsh destroy ' + host_name
    else:
        shutdown_cmd = 'virsh shutdown ' + host_name
    run_cmd_reout(shutdown_cmd)

# Set specified KVM to autostart when boot
def autostartVM(host_name) :
    if not isVMExist(host_name) :
        print('<<< ' + host_name + ' Not Exist! >>>')
        listAllKVM()
        return
    autostart_cmd = 'virsh autostart ' + host_name
    run_cmd_reout(autostart_cmd)
    # list all kvm exist status
    print('Autostart virtual machine list in the following')
    run_cmd_reout('virsh list --autostart --all')

# disable autostart kvm
def disableAutostartVM(host_name) :
    if not isVMExist(host_name) :
        print('<<< ' + host_name + ' Not Exist! >>>')
        listAllKVM()
        return
    autostart_cmd = 'virsh autostart --disable ' + host_name
    run_cmd_reout(autostart_cmd)
    # list all kvm exist status
    print('Autostart virtual machine list in the following')
    run_cmd_reout('virsh list --autostart --all')

# Clone kvm from template
def cloneVM(host_name, template) :
    if isVMRunning(template) :
        print(template + ' must to be shutdown to be clone!')
        return
    clone_cmd = 'virt-clone --force --original=' + template + ' --name=' + host_name + ' --file=' + image_path + host_name + '.qcow2'
    run_cmd_reout(clone_cmd)

# Sysprep kvm
def sysprepVM(new_host_name, old_host_name, miniClear = False) :
    if isVMRunning(old_host_name) :
        print(old_host_name + ' must to be shutdown to be clone!')
        return
    sysprep_cmd = ''
    if miniClear :
        sysprep_cmd = 'sudo virt-sysprep -d ' + old_host_name + ' --hostname ' + new_host_name + ' --operations customize,dhcp-client-state,dhcp-server-state,machine-id,net-hostname,net-hwaddr'
    else :
        sysprep_cmd = 'sudo virt-sysprep -d ' + old_host_name + ' --hostname ' + new_host_name + ' --operations defaults,-ssh-hostkeys'
    run_cmd_reout(sysprep_cmd)


# Remove specified vm define
def undefineVM(host_name, isforce=False) :
    if isVMRunning(host_name) :
        shutdownVM(host_name)
    if isforce :
        run_cmd_reout('virsh destroy ' + host_name)
    undefine_cmd = 'virsh undefine ' + host_name
    run_cmd_reout(undefine_cmd, goOnRun=True)

# Delete specified vm from disk
def deleteVM(host_name, isforce=False) :
    for path in getDiskList(host_name) :
        if path[len(path) - 4 :] != '.ISO' or path[len(path) - 4 :] != '.iso' :
            delete_cmd = 'sudo rm -rf ' + path
            run_cmd_reout(delete_cmd)
    undefineVM(host_name, isforce)
    return (host_name not in hostNameList())

# attach interface to vm
def addInterface(host_name) :
    addif_cmd = 'virsh attach-interface ' + host_name + ' --type bridge --source br0 --model virtio --persistent'
    run_cmd_reout(addif_cmd)

# Originally create kvm from iso image
def createVM(host_name, ram, vcpu, disk, os_type, iso) :
    if isVMExist(host_name) :
        print('<<< ' + host_name + ' has exist!' + '>>>')
        return
    create_cmd = 'virt-install \
            --virt-type=kvm \
            --name=' + host_name + ' \
            --ram=' + str(ram) + ' \
            --vcpus=' + str(vcpu) + ' \
            --os-variant=' + os_type + ' \
            --hvm \
            --noautoconsole \
            --cdrom=' + iso + ' \
            --network=bridge=br0,model=virtio \
            --graphics vnc,listen=0.0.0.0 \
            --disk path=' + image_path + host_name + '.qcow2,size=' + str(disk) + ',bus=virtio,format=qcow2'
    run_cmd_reout(create_cmd)


# get key, value of dict from file, # as the comment
def getKeyValue(file_name, sep='='):
    arg_dict = {}
    with open(file_name, 'r') as text:
        for tline in text:
            if len(tline.strip()) != 0 and tline[0] != '#':
                tlink = tline.strip().split('#')[0].split(sep)
                if len(tlink) > 1:
                    arg_dict[tlink[0].strip()] = tlink[1].strip()
    return arg_dict


