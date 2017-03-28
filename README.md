# Ubuntu/Debian KVM manager for DUTOE

Usage：
```shell
export PATH=$PATH:~/kvmManage
```
add to your .bashrc or .bash_profile or /etc/profile


虚拟机相关的管理命令如下，为了方便调用，所有都以dut开头，可以通过输出dut之后双击tab来查看你需要的相关命令，如果有其他功能需求，可以向我提：

* `dut-createvm <your-host-name>` 创建名为<your-host-name>的虚拟机，统一规定自己创建的虚拟机以自己的姓名简拼开头，只能是英文，数字，短划线的组合，如wyl-master，暂时默认只创建ubuntu server 16.04版本的虚拟机1G内存，1核CPU。虚拟机创建完之后会给你一个VNC端口号，可以通过VNC访问你的虚拟机。同时会给出IP和SSH端口号，通过ssh访问，SSH端口是22，默认禁用root登录。虚拟机的默认用户名和密码都是dutoe，自行修改。默认关闭防火墙。该命令需要sudo权限验证。
 
* `dut-createvm-2g-2core <your-host-name>`  创建名为<your-host-name>的虚拟机，并分配2G内存，2核心CPU。请在必要时再使用该命令创建。该命令需要sudo权限验证
 
* `dut-deletevm  <your-host-name>` [-f] 删除你的虚拟机，删除之前确认不要删成别人的了。删除之前会有提示，必须输入YES，其他任何输入都表示不删除。该命令需要sudo权限验证。[-f]为可选参数，强制删除虚拟机
 
* `dut-autostartvm  <your-host-name>`  将虚拟机设置为开机自动启动（即服务器启动时自动启动虚拟机）
 
* `dut-disableAutostartvm  <your-host-name>` 取消虚拟机的开机自动启动
 
* `dut-listvm`  显示所有虚拟机及其状态
 
* `dut-shutdownvm  <your-host-name>` [-f]  强制关闭虚拟机 可选的选项-f，当普通方法无法关机时使用-f，会丢失虚拟机中未保存的数据
 
* `dut-startvm  <your-host-name>` 手动启动虚拟机
 
* `dut-getvminfo  <your-host-name>` [-d] 查看虚拟机的基本信息，包括IP和VNC端口号，只有虚拟机运行期间才会有IP和VNC端口号，可选参数-d，获得虚拟机磁盘的详细信息，需要root权限
 
* `dut-clonevmfrom  <your-clone-from-host-name> <new-host-name>` 克隆虚拟机，第一个参数是被克隆的虚拟机名字，第二个参数是新克隆出来的虚拟机名字
 
* `dut-addinterface  <your-host-name>`  为虚拟机增加一块网卡，增加后的网卡直接进入虚拟机通过ifconfig -a即可可看

* `dut-adddisk  <your-host-name> size`  为虚拟机增加一块大小为size的硬盘，默认默认增加的硬盘在服务器的机械上

* `dut-originalvmcreate <config-file>`  创建你指定的内在大小、CPU个数、硬盘大小和系统光盘路径的虚拟机
config-file内容形如下：
```
# 根据以下内容创建你自己的虚拟机镜像，等号及等号前面的内容不能修改，它们的顺序可以随意，空格也可以忽略

hostname = wyl-original-vm  #虚拟机镜像名字，必须唯一，不能与系统中其他虚拟机重名，建议以自己名字的首字母开头
ram = 1024  #指定内存大小，单位是MB
vcpu = 1  #指定CPU个数
disk = 20  #指定磁盘大小，单位是GB
os_type = rhl7  #rhl7表示redhat7系列，可通过命令osinfo-query os查询，基本对应关系是ubuntu16.04就表示Ubuntu 16.04，centos7.0表示CentOS 7.0（其实与rhl7一样）
iso = /mnt/data/vhost/iso/centos7_mini.iso  #指定系统映像，为了方便其他人重用下载的映像，大家下载的映像路径统一放在/mnt/data/vhos/iso/
```
服务器根目录下有模板`original-kvm-config.ini`，可以自己cp一份，按需要修改

通常情况下IP不会变化，为了防止重启后IP变化，记得通过`dut-getvminfo`查看你的虚拟机IP，可以联系我在路由器中绑定你的虚拟机MAC跟IP。

VNC连接方法：
1.从REALVNC官方网站<https://www.realvnc.com/download/viewer/>下载VNC viewer安装，支持Windows和Linux
3.打开VNC viewer，输入`192.168.1.121:5901`即可连接5901对应的虚拟机，可以同时连接多个虚拟机

服务器用户名`dutoeserver`，密码`dutoeserver`，服务器IP为`192.168.1.121`。该账号仅用于虚拟机相关操作

指定静态ip的方法，修改`/etc/network/interfaces`内容如下，注意ens3改成你自己的网卡，ip地址改成你创建或启动虚拟机时路由器分配给你的地址，其他东西不用变：
```
auto ens3
iface ens3 inet static
address 192.168.1.125
netmask 255.255.255.0
gateway 192.168.1.2
dns-nameservers 192.168.1.2
```

