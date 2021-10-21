import requests, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--refreshtoken', required=True, metavar='freshtoken.txt', help='Refresh token to use')
parser.add_argument('-r', '--resource', required=True, metavar='api.spaces.skype.com', help='Resource to request access to')
parser.add_argument('-s', '--scope', required=False, default='openid', metavar='openid', help='Space-delimited list of permissions to request when the user is authorizing the application (default: openid)')
parser.add_argument('-c', '--client_id', required=False, default='d3590ed6-52b3-4102-aeff-aad2292ab01c', metavar='d3590ed6-52b3-4102-aeff-aad2292ab01c', help='The client ID of the target public OAuth application (default: d3590ed6-52b3-4102-aeff-aad2292ab01c)')
# TODO: do we need to url encode any spaces in the scope argument?
args = parser.parse_args()
refreshtoken_file = args.refreshtoken
resource = 'https://' + args.resource
resource_filename = args.resource.replace(".", "_")
requsted_scope = args.scope
client_id = args.client_id


def saveTokenToDisk(filename, token):
    f = open(filename, 'w')
    f.write(token)
    f.close()

try:
    with open(refreshtoken_file, 'r') as file:
        refreshtoken_content = file.read()
except IOError:
    print(f'[!] Refresh token file not found: {refreshtoken_file}')
    exit(1)

token_url = 'https://login.microsoftonline.com/Common/oauth2/token'
token_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
token_payload = {'client_id': client_id,
                 'grant_type': 'refresh_token',
                 'scope': requsted_scope,
                 'resource': resource,
                 'refresh_token': refreshtoken_content}


refreshtoken_response = requests.post(token_url, headers=token_headers, data=token_payload)

if refreshtoken_response.status_code == 200:
    newtokens = refreshtoken_response.json()
    scope = newtokens['scope']
    accesstoken = newtokens['access_token']
    freshtoken = newtokens['refresh_token']
    resource = newtokens['resource']
    print(f'[+] Scope: {scope}\n[+] Resource: {resource}\n[+] Access Token: {accesstoken} \n[+] Refresh Token: {freshtoken}')
    saveTokenToDisk(resource_filename + '_accesstoken.txt', accesstoken)
    saveTokenToDisk(resource_filename + '_freshtoken.txt', freshtoken)
    print(f'[+] Access token saved to: {resource_filename}_accesstoken.txt\n[+] Refresh token saved to: {resource_filename}_refreshtoken.txt')

else:
    # TODO: Better error handling
   print('[!] Something went wrong...')