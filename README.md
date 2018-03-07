ChainVeri_Sim
==============

# Overview
This project is ChainVeri blockchain simulation.

ChainVeri is a blockchain Based firmware verification system.
 
This project is helps to mesure the overhead to verify firmware integrity. 

# Reqirements
* Python3.6 or + 
* pipenv for virtual and isolated enviroment(recommends)
* Flask Python package (Make sure that packages installed for Python3 or +)
* REST API test tool(e.g POSTMAN for develop and cURL for IoT device)
* cURL(for automated IoT device testing)

# Installation
* git clone
* pip install pipenv
* pipenv --python=python3.6
* pipenv install 

# Usage
## For Simple test run
Just run CahinVeri_sim.run for basic simulation test.

## For independent run
* run ChainVeri Blockchain server: pipenv run python chainVeri_sim.py
* to chainge listening port use -p or --port option
   e.g pipenv run python blockchain.py -p 5001

# Files 
* README.md: This file.
* LICENSE: Clarify source licence.
* ChainVeri_sim.run: Define simulation scenario.
* ChainVeri_sim.py: runs Trader which maintain blockchain. 
* IoT_device.py: simulates IoT devices. In this file, IoT device connect to Trader.

# Project Member
 * Jea-Min Lim (jmlim@os.korea.ac.kr) 
 
# Appendix
This section describe extra information based on Ubuntu 17.10.
 
## How to install python 3, ,pip, pipenv for Ubuntu 17.10, Raspbian
 * Python 3 : use 'apt install python3'' and 'apt update'
 * pip : apt install python-pip
 * pipenv: use 'pip install pipenv' and excute echo "PATH=$HOME/.local/bin:$PATH" >> ~/.profile
    execute source ~/.profile and then 'pipenv install' to install pipenv.
    
## Available APIs
ChainVeri_sim use REST APIs
* URL/mine: request to create a block with given IoT device Info
* URL/transactions/new: send new transaction Infos
* URL/chain: request block info since genesis block
* URL/nodes/register: add reqested node as a member node
* URL/nodes/resolve: check Blockchain conflict between nodes
See APIs.md for detailed descriptions.
