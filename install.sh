#!/bin/bash
mkdir ~/.wallpapers & 
sudo cp -r ./py/* /usr/local/bin/ &&\
sudo cp -r ./src/* /usr/local/bin/ &&\
sudo cp ./wp ./wpg /usr/local/bin &&\
sudo cp ./functions /usr/local/bin &&\
sudo chmod +x /usr/local/bin/wpg && sudo chmod +x /usr/local/bin/wp
