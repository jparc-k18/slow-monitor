#!/bin/sh

ssh="sshpass -f $HOME/.pswd"

$ssh ssh -o PubkeyAuthentication=no hayashu@login.cc.kek.jp \
     ls -la /hsm/had/sks/E70/JPARC2025Jan/e70_2025jan \
     > /mnt/raid/subdata/influxdb/ls-kekcc/ls-kekcc-e70_2025jan

$ssh ssh -o PubkeyAuthentication=no hayashu@login.cc.kek.jp \
     ls -la /hsm/had/sks/E96/JPARC2025Jan/e96_2025jan \
     > /mnt/raid/subdata/influxdb/ls-kekcc/ls-kekcc-e96_2025jan
