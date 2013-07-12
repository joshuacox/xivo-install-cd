#!/bin/bash
set -x

build_dir=$(pwd)
image_dir="$build_dir/images"
packages_dir="/tmp/xivo_packages"
mirror="http://http.debian.net/debian"

cleanup () {
    rm -rf $build_dir/tmp/{cd-build,debian-cd,debootstrap,extra}
    rm -rf $build_dir/images/*
}

build_iso () {
    cd $build_dir
    ./get-xivo-packages.py $packages_dir
    simple-cdd --dist squeeze -g --profiles-udeb-dist squeeze --conf ./xivo.conf --debian-mirror $mirror
}

rename_iso () {
    cd $image_dir
    mv debian-*.iso $version.iso
    md5sum $version.iso > $version.iso.md5sum
}

version="squeeze-xivo-skaro-$(apt-cache policy pf-xivo | grep Candidate | grep -oE '[0-9]{2}\.[0-9]+' | head -n1)"

cleanup
build_iso
rename_iso
