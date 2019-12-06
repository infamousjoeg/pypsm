# pyPSM

CyberArk Privileged Session Manager RDPFile Generator for Python 3

## Usage

### Supported Parameters

* base_uri _(required)_
* username _(required)_
* password _(required)_
* address _(required)_
* authtype _(cyberark, ldap, windows, radius)_
* otpmode _(required if `authtype='radius'` - push, ~~challenge~~, append - default: push)_
* otp _(required if `authtype='radius'` and `otpmode=challenge` or `otpmode=append`)_
* platformid _(default: PSMSecureConnect)_
* verify _(default: `True`)_

### Generate RDPFile for PSM-RDP Connections

```python
from pypsm import RDP

# Configure the connection details
psmconnect = RDP(base_uri='https://cyberark.joegarcia.dev/', username='user', password='password123', address='10.0.4.48', authtype='radius', otpmode='push')
# Retrieve RDPFile data from CyberArk and create `connect.rdp` locally
psmconnect.connect()
```

### Secure Handling of Username + Password

It is recommended to use environment variables within the script that can be populated at runtime.  These should not be placed into script variables and should be used just-in-time (JiT).

## License

MIT