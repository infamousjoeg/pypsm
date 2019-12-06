#!/bin/bash

echo -e "\n\nTesting LDAP authentication...\n\n"
pushd tests/ || exit 1
    summon -e ldap python ldap.py
popd || exit 1

echo -e "\n\nTesting RADIUS Challenge/Response MFA authentication...\n\n"
pushd tests/ || exit 1
    summon -e radius python radius.py
popd || exit 1