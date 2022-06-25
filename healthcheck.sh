#!/bin/bash

get_log(){
	local _server=$1
    local _base_dir_log=/data/s1001/bin/log

    echo "$_server"

    # get recent log file
    go=$(ls ${_base_dir_log} -tr | grep -E "${_server}[-_0-9\.log]+$" | tail -n 1)
    local _recent_log_file=$go

    logs=$(tail -n 5 $_base_dir_log/$_recent_log_file)

    echo $logs
}

send_mail(){
    domain=verification.gnome-hub.com
    api_key=7d28e6a1eb12151868987af95616b7f1-8d821f0c-1aeed30e
    subject="Server Healthcheck Down Detected"
    local _message=$1
    to="alfianvansykes@gmail.com"
    from='Gnome Automation <automation@verification.gnome-hub.com>'
    url="https://api.mailgun.net/v3/$domain/messages"
    req="curl -g --user 'api:${api_key}' '$url' -F from='${from}' -F to='${to}' -F subject='${subject}' -F html=\"${message}\""
    eval "$req"
    exit 0;
}

send_discord(){
    webhook_url=https://discord.com/api/webhooks/990288785587707934/rPLMgznwPKHxRhlnzcILJgP_YjyVQaKcS_mnaLpXU6NWsY3WaPsPg9llgFibWVXB-0j_
    subject="!!!Server Healthcheck Down Detected!!!"
    local _message=$1
    req="curl -H 'Content-Type: application/json' -d '{\"username\": \"Gnome-Automation\", \"content\": \"${subject}\nCC: <@&983558291261112370> <@&983549809409552445>\n\n${message}\"}' $webhook_url"
    eval "$req"
    exit 0;
}

lcomma() { 
    sed '$x;$G;/\(.*\),/!H;//!{$!d};$!x;$s//\1/;s/^\n//'
}

echo "get server-list..."
IFS=" " read -r -a SERVER_LISTS <<< "loginserver versionserver fmserver idipserver worldserver teamserver routerserver crossgameserver dbserver gameserver gateserver masterserver controlserver"

iteration=0
down_count=0
up_count=0
serverlength=${#SERVER_LISTS[@]}
string_logs=''
string_server=''
for((i=0; i<serverlength; i++))
do
    echo "Checking ${SERVER_LISTS[$i]}..."
    cmd1="ps -Ao pid= -o comm= "
    cmd2="grep ${SERVER_LISTS[$i]}"
    is_server_running=$(eval "$cmd1" | eval "$cmd2")
    if [ -z "${is_server_running}" ]; then
        # get log and send alert via email
        timestamp=$(date '+%Y-%m-%d %H:%M:%S %Z')
        echo -e "!!! CAUGHT SERVER DOWN: ${SERVER_LISTS[$i]}\n"
        string_server+=${SERVER_LISTS[$i]}
        cmd3="get_log ${SERVER_LISTS[$i]}"
        logs=$(eval "$cmd3")
        string_logs+="$timestamp || ${SERVER_LISTS[$i]}=======<br><br>$logs<br><br>"
        down_count=$((down_count+1))
    else
        echo -e "Server ${SERVER_LISTS[$i]} OK!\n"
        up_count=$((up_count+1))
    fi
    iteration=$((iteration+1))
    sleep 1
done

echo -e "All checked servers: $iteration"
echo -e "Server down: $down_count\nServer up: $up_count\n"
stats="Server down: $down_count<br>Server up: $up_count<br>"
string_server=$(echo "$string_server" | lcomma)
server_affected=$string_server


if [ -z "${server_affected}" ]; then
    # nothing to do
    echo "nothing to do"
    exit 0;
else
    # if server affcted > 0, send email
    message="=====Stats=====<br><br>$stats<br><br>Server down lists: $server_affected<br><br>======LOGS=======<br><br>$string_logs"
    send_discord "$message"
    send_mail "$message"
fi




