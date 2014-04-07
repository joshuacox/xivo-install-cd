#!/bin/bash
set -x

build_dir=$(pwd)
image_dir="$build_dir/images"
packages_dir="/tmp/xivo_packages"
mirror="http://http.us.debian.org/debian"

cleanup () {
    rm -rf $build_dir/tmp/{cd-build,debian-cd,debootstrap,extra}
    rm -rf $build_dir/images/*
}

build_iso () {
    cd $build_dir
    ./get-xivo-packages.py $packages_dir -V rc
    simple-cdd --dist wheezy -g --profiles-udeb-dist wheezy --conf ./xivo.conf --debian-mirror $mirror
    if [ $? -ne 0 ] ; then
        exit 1
    fi
}

rename_iso () {
    cd $image_dir
    mv debian-*.iso $version.iso
    md5sum $version.iso > $version.iso.md5sum
}

version="xivo-$(apt-cache policy xivo | grep Candidate | grep -oE '[0-9]{2}\.[0-9]+' | head -n1)"

cleanup
build_iso
rename_iso
