'''
DNA_CENTER_DEBUG - Tells the SDK whether to log request and response information. Useful for debugging and seeing what is going on under the hood. Defaults to False.
DNA_CENTER_VERSION - DNA Center API version to use. Defaults to '2.1.1'.
DNA_CENTER_ENCODED_AUTH - It takes priority. It is the username:password encoded in base 64. For example ZGV2bmV0dXNlcjpDaXNjbzEyMyE which decoded is devnetuser:Cisco123!
DNA_CENTER_USERNAME - HTTP Basic Auth username.
DNA_CENTER_PASSWORD - HTTP Basic Auth password.
DNA_CENTER_BASE_URL - The base URL to be prefixed to the individual API endpoint suffixes. Defaults to https://sandboxdnac2.cisco.com:443.
DNA_CENTER_SINGLE_REQUEST_TIMEOUT - Timeout (in seconds) for RESTful HTTP requests. Defaults to 60.
DNA_CENTER_WAIT_ON_RATE_LIMIT - Enables or disables automatic rate-limit handling. Defaults to True.
DNA_CENTER_VERIFY - Controls whether to verify the server's TLS certificate or not. Defaults to True.
'''

from dnacentersdk import DNACenterAPI

dnac_creds = {}
dnac_creds['url'] = 'https://sandboxdnac2.cisco.com'
dnac_creds['username'] = 'devnetuser'
dnac_creds['password'] = 'Cisco123!'


if __name__ == '__main__':
    dnac = DNACenterAPI(username=dnac_creds['username'], password=dnac_creds['password'], base_url=dnac_creds['url'])
    print("Auth Token: ", dnac.access_token)