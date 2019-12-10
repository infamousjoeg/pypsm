import http.client
import json
import mimetypes
import ssl


class RDP(object):

    def __init__(self, base_uri, username, password, address, otpmode='push', otp=None, authtype='cyberark', platformid='PSMSecureConnect', logonto=None, verify=True):

        # Declare variables for self
        self._base_uri = base_uri.rstrip('/').replace('https://','')
        self._username = username
        self._password = password
        self._type = authtype.lower()
        self._otpmode = otpmode.lower()

        if (self._otpmode != 'challenge' and self._otpmode != 'append' and self._otpmode != 'push') and self._type == 'radius':
            raise Exception('only "challenge", "append", or "push" accepted for otpmode value')
            exit()
        
        self._otp = otp

        if not isinstance(self._otp, int) and (self._type == 'radius' and self._type == 'challenge'):
            raise Exception('provide a valid integer value for otp')

        self._address = address
        self._platformid = platformid
        self._conncomp = 'PSM-RDP'
        self._headers = {'Content-Type': 'application/json'}
        self._logonto = logonto
        self._verify = verify


    def _apiconnect(self, method, endpoint, payload, headers, parse=True):

        if self._verify:
            conn = http.client.HTTPSConnection(self._base_uri)
        else:
            conn = http.client.HTTPSConnection(self._base_uri, context=ssl._create_unverified_context)

        conn.request(method, endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()

        if parse:
            data_parsed = json.loads(data.decode('utf-8'))
        else:
            data_parsed = data
        
        return data_parsed


    def _logon(self):
        # CyberArk, LDAP, Windows Authentication Types
        if self._type == 'cyberark' or self._type == 'ldap' or self._type == 'windows':
            # Setup connection request for authentication
            payload = """{{
                "Username": "{}",
                "Password": "{}"
            }}""".format(self._username, self._password)
            url = "/PasswordVault/api/auth/{}/logon".format(self._type)
            response = self._apiconnect("POST", url, payload, self._headers)

            try:
                # If error is received...
                if response['ErrorCode']:
                    raise Exception('[{}] {}'.format(response['ErrorCode'],response['ErrorMessage']))
                    exit()
            except:
                # Token received and added to Authorization in header
                self._headers['Authorization'] = response

        elif self._type == 'radius' and self._otpmode == 'push':
            # Attempt RADIUS w/ username + password ONLY
            payload = """{{
                "Username": "{}",
                "Password": "{}"
            }}""".format(self._username, self._password)
            url = "/PasswordVault/api/auth/radius/logon"
            response = self._apiconnect("POST", url, payload, self._headers)

            try:
                # If error is received...
                if response['ErrorCode'] == 'ITATS542I':
                    raise Exception('[{}] otp and otpmode are required')
                    exit()
                elif response['ErrorCode']:
                    raise Exception('[{}] {}'.format(response['ErrorCode'],response['ErrorMessage']))
                    exit()
            except:
                # Token received and added to Authorization in header
                self._headers['Authorization'] = response

        # elif self._type == 'radius' and self._otpmode == 'challenge':
        #     payload = """{{
        #         "Username": "{}",
        #         "Password": "{}"
        #     }}""".format(self._username, self._password)
        #     url = "/PasswordVault/api/auth/radius/logon"
        #     response = self._apiconnect("POST", url, payload, self._headers)

        #     try:
        #         if response['ErrorCode'] == 'ITATS542I':
        #             # Second Factor Authentication - switch password to otp code
        #             payload = """{{
        #                 "Username": "{}",
        #                 "Password": "{}"
        #             }}""".format(self._username, self._otp)
        #             url = "/PasswordVault/api/auth/radius/logon"
        #             response = self._apiconnect("POST", url, payload, self._headers)
        #         elif response['ErrorCode']:
        #             raise Exception('[{}] {}'.format(response['ErrorCode'],response['ErrorMessage']))
        #             exit()
        #         else:
        #             # Token received and added to Authorization in header
        #             self._headers['Authorization'] = response
        #     except:
        #         raise Exception('an unknown error occurred during 2nd factor attempt')
        #         exit()

        elif self._type == 'radius' and self._otpmode == 'append':
            payload = """{{
                "Username": "{}",
                "Password": "{},{}"
            }}""".format(self._username, self._password, self._otp)
            url = "/PasswordVault/api/auth/radius/logon"
            response = self._apiconnect("POST", url, payload, self._headers)

            try:
                # If error is received...
                if response['ErrorCode']:
                    raise Exception('[{}] {}'.format(response['ErrorCode'],response['ErrorMessage']))
                    exit()
            except:
                # Token received and added to Authorization in header
                self._headers['Authorization'] = response

        elif self._type == 'saml':
            raise Exception('saml authentication not currently supported')
            exit()

        else:
            raise Exception('unknown authentication type provided')
            exit()


    def connect(self):

        self._logon()

        if self._logonto:
            payload = """{{
            "Username": "{username}",
            "Secret": "{password}",
            "Address": "{address}",
            "PlatformId": "{platformid}",
            "extraFields": {{
                "LogonDomain": "{logonto}"
            }},
            "PSMConnectPreRequisites": {{
                "ConnectionComponent": "PSM-RDP"
            }}
        }}""".format(username=self._username, password=self._password, address=self._address, platformid=self._platformid, logonto=self._logonto)
        else:
            payload = """{{
                "Username": "{username}",
                "Secret": "{password}",
                "Address": "{address}",
                "PlatformId": "{platformid}",
                "PSMConnectPreRequisites": {{
                    "ConnectionComponent": "PSM-RDP"
                }}
            }}""".format(username=self._username, password=self._password, address=self._address, platformid=self._platformid)

        url = "/PasswordVault/api/Accounts/AdHocConnect"
        response = self._apiconnect("POST", url, payload, self._headers, parse=False)
        # Enable for MacOS RDP Client fix
        response += b'enablecredsspsupport:i:0'
        
        try:
            f = open('connect.rdp','wb+')
            f.write(response)
            f.close()
            print('connect.rdp created for connection')
        except Exception as e:
            raise Exception(e)
            exit()
