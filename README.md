# OAuth Device Code Authorization Phishing

Some scripts to utilise device code authorization for phishing.

High level overview as per the instructions as: https://o365blog.com/post/phishing/

1. An attacker connects to `/devicecode` endpoint and sends `client_id` and `resource`
2. After receiving `verification_uri` and `user_code`, create an email containing a link to verification_uri and user_code, and send it to the victim. (delivering the phishing email is not in scope for this project)
3. Victim clicks the link, provides the code and completes the sign in.
4. The attacker receives `access_token` and `refresh_token` and can now mimic the victim (Interact with the various Microsoft API endpoints to perform various tasks).

Some of the API endpoints include: 
+ Microsoft Graph: https://graph.microsoft.com
+ Microsoft 365 Mail API: https://outlook.office.com
+ Microsoft Skype & Teams API: https://api.spaces.skype.com
+ Azure Key Vault: https://vault.azure.net

__Note__: Uses __version 1.0__ which is different to v2.0 flow used in the documentation.

The official Microsoft Device Code Authorization Flow documentation can be found here: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code


## devicecode_phish.py

This script will first request the initial `user_code` from the Azure AD `devicecode` endpoint. Next, it will start polling Microsoft token endpoint (`login.microsoftonline.com/Common/oauth2/token?api-version=1.0`) for the authentication status using the `interval` value returned by the initial request (default every 5 seconds).

The script takes the following arguments:

| Argument | Default Value | Required or Optional | 
| --- | --- | --- |
| `-r` or `--resource` | graph.microsoft.com | Optional |
| `-c` or `--client_id` | d3590ed6-52b3-4102-aeff-aad2292ab01c | Optional |


Example: 

```
python3 devicecode_phish.py
[*] User code: PF2PSG7LW
[*] User code expires at: 2021-10-21 15:03:00.206630
[*] Polling Microsoft for user authentication...
[*] Status: authorization_pending at 14:48:00
```

The attacker will need to send the `verification_uri` (https://microsoft.com/devicelogin) URI to the victim. This is the URI the user should go to with the `user_code` (_PF2PSG7LW_ from the above example) in order to sign in.

> __Note__: If the user authenticates with a personal account (on /common or /consumers), they will be asked to sign in again in order to transfer authentication state to the device. They will also be asked to provide consent, to ensure they are aware of the permissions being granted. This does not apply to work or school accounts used to authenticate.


## refresh_tokens.py

This script is used to request new `access` & `refresh` tokens for different `resources` (Microsoft API endpoints). 

| Argument | Default Value | Required or Optional | 
| --- | --- | --- |
| `-t` or `--refreshtoken` | - | Required |
| `-r` or `--resource` | - | Required |
| `-s` or `--scope` | openid | Optional |
| `-c` or `--client_id` | d3590ed6-52b3-4102-aeff-aad2292ab01c | Optional |



## fetch_emails.py

Dump victims emails to file using an access token (must be valid for https://graph.microsoft.com resource).