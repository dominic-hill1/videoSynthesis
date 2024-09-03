sudo apt update
wget https://github.com/openframeworks/openFrameworks/releases/download/0.12.0/of_v0.12.0_linux64gcc6_release.tar.gz
tar -xvzf of_v0.12.0_linux64gcc6_release.tar.gz
cd of_v0.12.0_linux64gcc6_release/scripts/linux/ubuntu/
sudo ./install_dependencies.sh
sudo ./install_codecs.sh
cd ..
sudo apt install make
./compileOF.sh -j3
cd ../../apps/myApps/
git clone https://github.com/dominic-hill1/videoSynthesis.git
cd videoSynthesis
make clean
cd GUI
sudo apt install python3-pip
sudo apt-get install libxcb1 libxcb-keysyms1 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-xfixes0 libxcb-icccm4 libxcb-image0 libxcb-sync1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0
pip3 install pyqt5
pip3 install numpy
pip3 install serial
python3 main.py