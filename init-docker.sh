#/bin/bash

CD32=/tmp/cd32
CD64=/tmp/cd64
PACKAGES=/tmp/xivo_packages/

if [ $(id -u) -eq 0 ]; then

    if [ ! -d $CD32 ]; then
        mkdir -p $CD32/images
    fi

    if [ ! -d $CD64 ]; then
        mkdir -p $CD64/images
    fi

    if [ ! -d $PACKAGES ]; then
        mkdir $PACKAGES
    fi

    chmod 777 $CD32 $CD32/images $CD64 $CD64/images $PACKAGES
else
    echo "Please run as root or with sudo!"
fi
