
# pegass_auth
> A tiny client to manage your Sellsy plateform using Python

French Red Cross is currently using a tool named [Pegass](https://id.authentification.croix-rouge.fr/my.policy) to visualize, enroll to activities, monitor them and more... This application is carefully thought out, and the different views give you plenty options to display your data. However, my motivation was to extract Pegass data to analyze it and create some custom views. The application was not designed to let users get data out of the box (closed API, no CSV extract, ...). That's why I made this little module to help whoever wants to extract their data in a simple way through the Pegass API. :red_car: :red_car: :fire_engine: :fire_engine: :rotating_light: :rotating_light:

### Features
- Get authentication cookies to open Pegass API gate with your application credential
- Create an abstraction for requesting the API


## Installing
```shell
# Connect to your virtualenv
$  workon projectenv

# Use pip to install the package
$  pip install pegass_auth
```

Verify now if the package as been successfully installed
```shell
$  python
>> import pegass_auth # Should not raise exception
```

## Quick Start

### Get authentication cookies to make requests out of the box

```python
import os
import requests
import pegass_auth

username = os.environ['username']
password = os.environ['password']

auth_cookies = pegass_auth.login(username, password)

# When using 'requests' package
r = requests.get('{}/crf/rest/gestiondesdroits'.format(pegass_auth.DEFAULT_PEGASS_URL), cookies=auth_cookies)

if r.status_code == 200:
    print(r.json())
else:
    print('Request went wrong ! Status code returned : {}'.format(r.status_code))     
```


### Using package abstraction to make request

The package gives you two ways to make a request to Pegass API :
- Using cookies :
```python
import os
import pegass_auth as pegass

auth_cookies = login(os.environ['username'], os.environ['password'])
rules = pegass.request('crf/rest/gestiondesdroits', cookies=auth_cookies)
print(rules)
```

- Using credentials:
```python
import os
import pegass_auth as pegass

username = os.environ['username']
password = os.environ['password']
rules = pegass.request('crf/rest/gestiondesdroits', username=username, password=password)
print(rules)
```
**Note**: The last way to make request (the one with *username* and *password*) runs each time the ```login``` logic. Make *cookies* methods your first choice if you need to do multiple API requests.

All the previous codes prints the following response:
```json
{
   'utilisateur':{
      'id':'01XXXXXXXX',
      'structure':{
         'id':1XXX,
         'typeStructure':'UL',
         'libelle':'UNITE LOCALE DE XXXXXXX',
         'libelleCourt':'XX',
         'adresse':'XX XXXXXXXXXXXXXXXX XXXXXX XXXX XXXXXXXX',
         'telephone':'X XX XX XX XX',
         'mail':'ul.XXXXXXXXX@croix-rouge.fr',
         'siteWeb':'XXXXXXXXXXXX.croix-rouge.fr/XXXXXXXX/',
         'parent':{
            'id':XX
         },
         'structureMenantActiviteList':[
            {
               'id':1XXX,
               'libelle':'UNITE LOCALE DE XXXXXXX'
            }
         ]
      },
      'nom':'Foo',
      'prenom':'Bar',
      'actif':True,
      'mineur':False
   },
   'structuresAdministrees':[

   ]
}
```

## Pegass API Endpoints
I've started to do a reverse engineering on Pegass app to list the API endpoints I need in order to achieve my personal app.

## Error handler
Their is no error handler implemented yet in the package.


## Links

- [Pegass](https://id.authentification.croix-rouge.fr/my.policy)
- [pegass_auth issue tracker](https://github.com/Annouar/pegass_auth/issues)
- [French Red Cross](https://www.croix-rouge.fr/)


## License

 - **MIT** : http://opensource.org/licenses/MIT