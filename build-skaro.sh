#!/bin/bash

build_dir="/home/builder/install_cd"
image_dir="$build_dir/images"
packages_dir="/tmp/xivo_packages"
mirror="http://ftp.ca.debian.org/debian"
#mirror="http://127.0.0.1:3142/debian"

cleanup () {
    #rm -rf $packages_dir/*
    rm -rf $build_dir/tmp/{cd-build,debian-cd,debootstrap,extra}
    rm -rf $build_dir/images/*
}

build_iso () {
    cd $build_dir
    su builder -c "./get-xivo-packages.py -s skaro $packages_dir"
    su builder -c "simple-cdd --dist squeeze -g --profiles-udeb-dist squeeze --conf ./xivo.conf --debian-mirror $mirror"
}

deploy_iso () {
    cd $image_dir
    mv debian-6.0.4-i386-CD-1.iso $version.iso
    md5sum $version.iso > $version.iso.md5sum
    rsync -av $image_dir/ mirror.xivo.fr:/data/iso/$version/
}

cd $build_dir
for flavour in prod; do
    case $flavour in
        "prod") branch="production";;
        *     ) 'not supported';;
    esac
    release="squeeze-xivo-skaro-1.2"
    version="squeeze-xivo-skaro-$(apt-cache policy pf-xivo | grep Candidate | grep -Eo '1\.[2-9]\.[0-9]{1,2}')"
    cleanup
    build_iso
    deploy_iso
done
