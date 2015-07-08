#!/bin/sh

CD32=/tmp/cd32
CD64=/tmp/cd64
PACKAGES=/tmp/xivo_packages/

install -m 777 -d $CD32
install -m 777 -d $CD32/images
install -m 777 -d $CD64
install -m 777 -d $CD64/images
install -m 777 -d $PACKAGES
