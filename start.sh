#!/bin/bash

#!/bin/bash

echo "Starting smartpot setup...."
export DOCKER_USER="$(id root -u):$(id -g)"
ini_file="smartpot.ini"
log_file="smartpot.log"
data_dile="data.csv"

echo "Checking if configuration file is existent"
#check if smartpot.ini is existent
if [[ ! -f $ini_file ]]; then
    echo "Configuration file not found. Creating..."
    cp resource/smartpot.ini smartpot.ini
    echo "Please enter your telegram token: "
    read TOKEN
    echo "Please enter yout chatid: "
    read ID
    sed -i "s/token = */token = $TOKEN/g" smarpot.ini
    sed -i "s/chatid = */chatid = $ID/g" smartpot.ini
fi;

echo "Checking if logfile is existent..."
if [[! -f $log_file]]; then
    echo "Logfile not found. Creating..."
    touch $log_file
fi;

echo "Checking if logfile is existent..."
if [[! -f $data_file]]; then
    echo "Datafile not found. Creating..."
    touch $data_file
fi;
