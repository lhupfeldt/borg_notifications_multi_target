#!/bin/bash

set -u


function add_client() {
    client_type=$1
    client_user_name=$2
    client_public_key_file=$3

    server_account="bbackup"
    backup_root="/home"

    home_dir=$backup_root/$server_account
    client_repo=$home_dir/repos/$client_user_name
    authorized_keys=$home_dir/.ssh/authorized_keys

    client_public_key=$(cat $client_public_key_file)

    # TODO: This does not handle changed commands
    sudo grep "$client_public_key" $authorized_keys || {
        if [ $client_type == "append" ] ; then
            client_type_args="--append-only "
        elif [ $client_type == "cleanup" ] ; then
            client_type_args=""
        else
            echo "Expected 'append' or 'cleanup', got $client_type" 1>&2
            exit 1
        fi

        cmd="command=\"cd $client_repo; borg serve $client_type_args --restrict-to-path $client_repo\",no-port-forwarding,no-X11-forwarding,no-pty,no-agent-forwarding,no-user-rc $client_public_key"
        echo "$cmd" | sudo tee -a $authorized_keys
    }

    sudo mkdir -p $client_repo
    sudo chown $server_account:$server_account $client_repo
    sudo chmod 700 $client_repo
}


add_client $1 $2 $3
