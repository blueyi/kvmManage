# Ubuntu/Debian KVM manager for DUTOE

export PATH=$PATH:~/kvmManage

add to your .bashrc or .bash_profile or /etc/profile



虚拟机相关的管理命令如下，为了方便调用，所以都以dut开头，可以通过输出dut之后双击tab来查看你需要的相关命令，如果有其他功能需求，可以向我提：

dut-createvm <your-host-name> 创建名为<your-host-name>的虚拟机，统一规定自己创建的虚拟机以自己的姓名简拼开头，只能是英文，数字，短划线的组合，如wyl-master，暂时默认只创建ubuntu server 16.04版本的虚拟机1G内存，1核CPU。虚拟机创建完之后会给你一个VNC端口号，可以通过VNC访问你的虚拟机。同时会给出IP和SSH端口号，通过ssh访问，SSH端口是22，默认禁用root登录。虚拟机的默认用户名和密码都是dutoe，自行修改。默认关闭防火墙。该命令需要sudo权限验证。

dut-createvm-2g-2core <your-host-name>  创建名为<your-host-name>的虚拟机，并分配2G内存，2核心CPU。请在必要时再使用该命令创建。该命令需要sudo权限验证

dut-deletevm  <your-host-name> 删除你的虚拟机，删除之前确认不要删成别人的了。删除之前会有提示，必须输入YES，其他任何输入都表示不删除。该命令需要sudo权限验证。


dut-autostartvm  <your-host-name>  将虚拟机设置为开机自动启动（即服务器启动时自动启动虚拟机）

dut-disableAutostartvm  <your-host-name> 取消虚拟机的开机自动启动

dut-listvm  显示所有虚拟机及其状态

dut-shutdownvm  <your-host-name>  强制关闭虚拟机

dut-startvm  <your-host-name> 手动启动虚拟机

dut-vmVNCPort  <your-host-name>  查看虚拟机的VNC端口号，只有虚拟机运行期间才会有VNC端口号

dut-getvmip  <your-host-name> 查看虚拟机IP

通常情况下IP不会变化，为了防止重启后IP变化，记得通过dut-getvmip查看你的虚拟机IP，可以联系我在路由器中绑定你的虚拟机MAC跟IP。

VNC连接方法：
VNC需要通过SSH tunnel才能连接虚拟机，所以都需要建立SSH tunnel连接
Windows系统：
1.从REALVNC官方网站 https://www.realvnc.com/download/viewer/下载VNC viewer安装。
2.打开putty，Host name中输入服务器IP（192.168.1.121），端口默认22。点开左侧的SSH选项，点击Tunnels，source port中输入你想使用的本地端口，Destination中输入你需要建立隧道的本地IP和远程虚拟机的VNC监听端口，点击Add后，Open即可，此时需要输入服务器用户和密码（dutoeserver）。这样就建立好了SSH隧道。如果有多台虚拟机，则通过add一次可以添加多个监听隧道。如我有虚拟机3台，分别端口为5901、5902、5903，则我可以Source port中填写5901，然后Destination中填写127.0.0.1:5901，点击Add，其他两个端口类似添加。最后点击Open即可
3.打开VNC viewer，输入127.0.0.1:5901即可连接5901对应的虚拟机，可以同时连接多个虚拟机
暂时没有找到好的方法在不进入虚拟机的情况下获取其IP

服务器用户名dutoeserver，密码dutoeserver，服务器IP为192.168.1.121。该账号仅用于虚拟机相关操作
