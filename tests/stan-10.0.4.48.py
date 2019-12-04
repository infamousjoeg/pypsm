from pypsm import RDP
import os


psmtestconnect = RDP(
    base_uri    = os.environ.get('PYPSM_BASEURI'),
    username    = os.environ.get('PYPSM_USERNAME'),
    password    = os.environ.get('PYPSM_PASSWORD'),
    address     = os.environ.get('PYPSM_ADDRESS'),
    authtype    = os.environ.get('PYPSM_AUTHTYPE')
)

psmtestconnect.connect()

print('connect.rdp File Contents:')
print('==========================')
f = open('connect.rdp', 'rb')
for line in f:
    print(line)
f.close()