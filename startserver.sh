sudo iptables -A INPUT -p tcp --dport 77777 -j ACCEPT
sudo kill -9 $(lsof -t -i:77777)
DreamDaemon polaris 77777 -trusted -webclient -public
