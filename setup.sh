#!/bin/bash
echo  "export DOCKER_USER=\"$(id root -u):$(id -g)\"" >> ~/.bash_profile
source ~/.bash_profile

echo "Welcome to SmartPot"
echo "###################"
echo "Starting smartpot setup...."


ini_file="smartpot.ini"
log_file="smartpot.log"
data_file="data.csv"

function write_token() {
    echo -n "Please enter your telegram token: "
    read TOKEN
    echo -n "Please enter yout chatid: "
    read ID
    sed -i "s/token =.*/token = $TOKEN/g" smartpot.ini
    sed -i "s/chatid =.*/chatid = $ID/g" smartpot.ini
}

echo ""
echo "Checking if configuration file is existent..."
#check if smartpot.ini is existent
if [ ! -f $ini_file ]
then
    echo "Configuration file not found. Creating..."
    cp resources/smartpot.ini smartpot.ini
    write_token
else
    echo "Found configuration file"
    if [ "$(cat smartpot.ini | grep "<your-token>\|<your-chat-id>")" != "" ]
    then
      echo "It seems like you dont have configured your telgram token and chat-id..."
      write_token
    fi
fi

echo ""
echo "Checking if logfile is existent..."
if [ ! -f "$log_file" ];
then
    echo "Logfile not found. Creating..."
    touch $log_file
else
    echo "Found Logfile..."
fi;

echo ""
echo "Checking if logfile is existent..."
if [ ! -f $data_file ];
then
    echo "Datafile not found. Creating..."
    touch $data_file
else
    echo "Found Datafile"
fi;

echo ""
echo "Configuration of Logfile, Datafile and INI-File was successfull."
echo "You can now start the smartpot by calling:"
echo -e "\t docker-compose up"