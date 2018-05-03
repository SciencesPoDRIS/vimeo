# Vimeo
Collect metadata and download videos from multiple vimeo accounts.


## Dependencies

[PyVimeo lib](https://github.com/vimeo/vimeo.py)


## Install
Create a dedicated virtualenv

`> mkvirtualenv vimeo`

Install dependencies

`> pip install -r requirements.txt`

Copy the default conf file

`> cp conf.default.json conf.json`

Complete your conf.json file and add as many object as you need.
You will find your token on the [Vimeo app page](https://developer.vimeo.com/apps/)

1. Create your app
2. Edit your app
3. Click on the "Authentication" tab
4. Click on "Generate an Access Token"

The "Client Identifier" will be `token`.
The "Client Secrets" will be `key`.
The freshly generated "Token" will be `secret`.
Additionally, `name` will be the name that you wanna give to this account,
`email` should be the email address used to log to this accound and `link` should be the vimeo link to this account.


## Execution
`> workon vimeo`

# 
`> python script.py`


## Control quality



## Documentation
https://developer.vimeo.com/api/start


## Inspiration
https://github.com/yeeking/vimeo-account-downloader/blob/master/vimeo_backup.py


## Credits
[Sciences Po - Library](http://www.sciencespo.fr/bibliotheque/en)


## Licenses
[LGPL V3.0](http://www.gnu.org/licenses/lgpl.txt "LGPL V3.0")

[CECILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.html "CECILL-C")