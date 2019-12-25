#!/bin/bash

set -eux
# apt-get update
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" dist-upgrade
# install unzip, git
sudo apt-get install -y unzip git
# install tracer
sudo apt-get install strace ltrace
# install socat
sudo apt-get install socat
# install binutils
sudo apt-get install binutils
# install radare2
git clone https://github.com/radare/radare2 ~/radare2
sudo ~/radare2/sys/install.sh
# install pwndbg
sudo apt-get install -y gdb
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
cd ..
# install rp++
echo "export PATH=\$HOME/bin:\$PATH" >> ~/.bash_profile
mkdir ~/bin
wget https://github.com/downloads/0vercl0k/rp/rp-lin-x64 -O ~/bin/rp
# install checksec.sh
wget https://github.com/slimm609/checksec.sh/archive/master.tar.gz
tar zxvf master.tar.gz -C ~  && rm master.tar.gz
mv checksec.sh-master/checksec ~/bin/checksec
# package for x86
sudo dpkg --add-architecture i386
sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386
sudo apt-get install -y gcc-multilib g++-multilib
# install pwntools
sudo apt-get install -y python3 python3-dev python3-pip
pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
