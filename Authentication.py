from dnacentersdk import DNACenterAPI

dnac_creds = {}
dnac_creds['url'] = 'https://sandboxdnac2.cisco.com'
dnac_creds['username'] = 'devnetuser'
dnac_creds['password'] = 'Cisco123!'


dnac = DNACenterAPI(username= dnac_creds['username'] , password= dnac_creds['password'], base_url=dnac_creds['url'])
print("Auth Token: ", dnac.access_token)
