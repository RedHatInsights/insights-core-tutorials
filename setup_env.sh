#!/bin/sh
pckarr=(git gcc python3.6)
#yum update -y
for i in  ${pckarr[*]}
 do
   if yum list installed $i >/dev/null 2>&1;
   then
    echo Package  $i already installed
  else
    echo $i is not INSTALLED!!!!
    echo To install, please refer to https://insights-core_tutorials.readthedocs.io/en/latest/prep_tutorial_env.html
#    yum install $i -y
  fi
done


#updatedb

