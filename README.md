To setup on Seeed NPI I.MX6ULL board:

```
sudo apt install -y python3 python3-pip python3-venv
```
This will install python3.7.3 and pip3 18.1

```
git clone https://github.com/cstrutton/IMX-server
cd IMX-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirents.txt


Add Service Files

https://www.devdungeon.com/content/creating-systemd-service-files

sudo cp IMX-server.service /ect/systemd/system/IMX-server.service
sudo cp IMX-server.service /ect/systemd/system/IMX-server.service


###### Network Configuration ######

From: https://developer.toradex.com/knowledge-base/ethernet-network-(linux)

Using the interactive mode to configure a static Ethernet address

```
root@colibri-t30:~# connmanctl
connmanctl> config ethernet_00142d259a48_cable --ipv4 manual 192.168.10.2 255.255.255.0 192.168.10.1
connmanctl> exit
```
### Notes ###
https://forum.radxa.com/t/rock-pi-4b-v1-4-no-boot-on-emmc/3812
