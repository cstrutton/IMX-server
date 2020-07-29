## To setup on Seeed NPI I.MX6ULL board:

#### Install required packages:
```
sudo apt-get update
sudo apt install -y python3 python3-pip python3-venv openssh-server git
```
#### Setup python:

```
git clone https://github.com/cstrutton/IMX-server
cd IMX-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirents.txt
```

#### Add Service Files:

```
# create hard links to service files
sudo ln ./service_files/IMX-server.service /ect/systemd/system/IMX-server.service
sudo ln ./service_files/IMX-server-post-to-db.service /ect/systemd/system/IMX-server-post-to-db.service

# enable both services
sudo systemctl enable IMX-server
sudo systemctl enable IMX-server-post-to-db

# reload the configuration
sudo systemctl daemon-reload
```
#### Network Configuration:

Use connman interactive mode to configure the PLANT network:
```
root@npi:~# connmanctl
# Plug in the PLANT network and run 
connmanctl> services # prints out the name of the plant network
connmanctl> config ethernet_<mac-address>_cable --ipv4 manual 10.2.42.155 255.255.192.0 10.4.1.9
connmanctl> config ethernet_<mac-address>_cable --nameservers 10.4.1.200 10.5.1.200
connmanctl> exit
```
Use connman interactive mode to configure the PLC network:
```
root@npi:~# connmanctl
# Plug in the PLC network and run 
connmanctl> services # prints out the name of the networks
connmanctl> config ethernet_<mac-address>_cable --ipv4 manual 192.168.1.254 255.255.255.0
connmanctl> exit
```

## Notes:
- service files:
  - https://www.devdungeon.com/content/creating-systemd-service-files
  - https://www.freedesktop.org/software/systemd/man/systemd.service.html#

 - rock pi boot from emmc:
    - https://forum.radxa.com/t/rock-pi-4b-v1-4-no-boot-on-emmc/3812

- Network configuration with connman
  - https://developer.toradex.com/knowledge-base/ethernet-network-(linux)
  - http://variwiki.com/index.php?title=Static_IP_Address


## Static IP adresses:
|IP|Machine|MAC|
|-------------|------|-------------------|
| 10.4.42.153 | 1533 | d6:89:7c:ec:e0:9e |
| 10.4.42.154 | 1816 | 2e:1a:6d:d1:6f:1d |
| 10.4.42.155 |||
| 10.4.42.156 |||
| 10.4.42.157 |||
| 10.4.42.158 |||
| 10.4.42.160 |||
| 10.4.42.161 |||
| 10.4.42.162 |||
| 10.4.42.163 |||
| 10.4.42.164 |||
| 10.4.42.165 |||
| 10.4.42.166 |||
| 10.4.42.167 |||
| 10.4.42.168 |||
| 10.4.42.169 |||
