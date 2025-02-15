#!/bin/sh

ssh="sshpass -f $HOME/.pswd"

dir=/mnt/raid/subdata/influxdb/ls-kekcc

tmp=$dir/ls-kekcc-e70_2025jan
$ssh ssh -o PubkeyAuthentication=no hayashu@login.cc.kek.jp \
     ls -la --time-style=+%s /hsm/had/sks/E70/JPARC2025Jan/e70_2025jan \
     > $tmp
grep run $tmp | tail -n1 | awk '{print "kekcc,data_dir=e70_2025jan permission=\"" $1 "\",runnumber=" substr($7, 4, length($7)-7) "i " $6*1e9}'

tmp=$dir/ls-kekcc-e96_2025jan
$ssh ssh -o PubkeyAuthentication=no hayashu@login.cc.kek.jp \
     ls -la --time-style=+%s /hsm/had/sks/E96/JPARC2025Jan/e96_2025jan \
     > $tmp
grep run $tmp | tail -n1 | awk '{print "kekcc,data_dir=e96_2025jan permission=\"" $1 "\",runnumber=" substr($7, 4, length($7)-7) "i " $6*1e9}'
