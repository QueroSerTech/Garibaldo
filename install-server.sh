#!/bin/bash

git clone https://github.com/msfidelis/google.git
cd google 
python setup.py install
rm -rf google