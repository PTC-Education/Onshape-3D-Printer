from OnshapePlus import *

try:
    try:
        exec(open('../apikeys.py').read())
        base = 'https://cad.onshape.com'
        client = Client(configuration={"base_url": base,
                                    "access_key": access,
                                    "secret_key": secret})
        print('client configured')
    except:
        exec(open('apikeys.py').read())
        base = 'https://cad.onshape.com'
        client = Client(configuration={"base_url": base,
                                    "access_key": access,
                                    "secret_key": secret})
        print('client configured')
except:
    print('Api keys file not found. Input keys manually.')
    access = input('Please enter your access key: ')
    secret = input('Please enter your secret key: ')
    base = 'https://cad.onshape.com'
    client = Client(configuration={"base_url": base,
                                "access_key": access,
                                "secret_key": secret})
    print('client configured')

try:
    print(documents(client))
except:
    print('fail')