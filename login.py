import os
import sys



def _hash(s):
    h = 0
    for c in s:
        c = ord(c)
        h = ((h << 5) - h) + c
    return str(h)

def create_apikey(s):
    api_key = _hash(s)
    while len(api_key) < 32:
        s = s[1:-1]
        api_key += _hash(s)
    return api_key[:32]



if len(sys.argv) != 3:
    print('Usage: hajau login <username> <password>')
else:
    username = sys.argv[1]
    password = sys.argv[2]
    api_key = create_apikey(username + '$$$' + password)
    api_path = os.path.expanduser('~/.remote_log.api')
    with open(api_path, 'w') as file:
        file.write(api_key)
    print("API key is: {}, stored at ~/.remote_log.api".format(api_key))