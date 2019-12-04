#!/bin/bash

echo -e "\n\nTesting LDAP authentication...\n\n"
summon -e ldap python ldap.py

echo -e "\n\nTesting RADIUS Challenge/Response MFA authentication...\n\n"
summon -e radius python radius.py