#!/bin/bash
set -x

build_dir=$(pwd)
image_dir="$build_dir/images"
packages_dir="/tmp/xivo_packages"
mirror="http://ftp.ca.debian.org/debian"

cleanup () {
    rm -rf $build_dir/tmp/{cd-build,debian-cd,debootstrap,extra}
    rm -rf $build_dir/images/*
}

build_iso () {
    cd $build_dir
    ./get-xivo-packages.py -s skaro $packages_dir
    simple-cdd --dist squeeze -g --profiles-udeb-dist squeeze --conf ./xivo.conf --debian-mirror $mirror
}

rename_iso () {
    cd $image_dir
    mv debian-6.0.4-i386-CD-1.iso $version.iso
    md5sum $version.iso > $version.iso.md5sum
}

release="squeeze-xivo-skaro-1.2"
version="squeeze-xivo-skaro-$(apt-cache policy pf-xivo | grep Candidate | grep -Eo '1\.[2-9]\.[0-9]{1,2}')"

cleanup
build_iso
rename_iso
