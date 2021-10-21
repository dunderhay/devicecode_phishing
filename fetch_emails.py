import requests, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--accesstoken', required=True, metavar='initial_accesstoken.txt', help='Access token to use (must be valid for graph.microsoft.com API resource)')
args = parser.parse_args()
accesstoken_file = args.accesstoken

try:
    with open(accesstoken_file, 'r') as file:
        accesstoken_content = file.read()
except IOError:
    print(f'[!] Access token file not found: {accesstoken_file}')
    exit(1)


msgraph_url = 'https://graph.microsoft.com/v1.0/me/messages'
msgraph_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                   'Authorization': 'Bearer ' + accesstoken_content}


getemails_response = requests.get(msgraph_url, headers=msgraph_headers)

if getemails_response.status_code == 200:
    email_content = getemails_response.text
    print('[+] Writing email to file: email.txt')
    f = open('email.txt', 'w')
    f.write(email_content)
    f.close()

else:
    # TODO: Better error handling
    print('[!] Something went wrong...')