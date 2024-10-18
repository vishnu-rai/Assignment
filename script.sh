#!/bin/bash

#number of folder
n=5
BASE_FOLDER='folder'

for ((i=1; i<=n; i++))
do
    #individual folder names
    FOLDER_NAME="${BASE_FOLDER}_${i}"
    #creating the folder
    mkdir -p "$FOLDER_NAME"
    #writing into the json file 
    cat <<EOF > "$FOLDER_NAME/param.json"
{
    "folder_name": "$FOLDER_NAME"
}
EOF
    echo "Folder '$FOLDER_NAME' and file 'param.json' created."
done
