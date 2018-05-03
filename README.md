# Vimeo
Collect metadata and download videos from multiple [Vimeo](https://vimeo.com/) accounts.


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

Additionally, `name` will be the name that you wanna give to this account.

`email` should be the email address used to log to this accound.

And `link` should be the vimeo link to this account.


## Execution
`> workon vimeo`

# Run script to download videos
`> python script.py`

# Run script to check the quality
`> python check.py`


## Control quality
The control quality should be the "check_videos.csv" file.

`id` : Unique identifier of the video. Created by Vimeo.

`name` : Title of the video.

`url` : Url of the video.

`account` : Name of the user account that uploaded the video.

`video_downloaded` : `1` if the video has been downloaded, else `0`.

`metadata_downloaded` : `1` if the metadata file has been dowloaed, else `0`.

`video_md5_vimeo` : MD5 of this video according to Vimeo.

`video_md5_calculated` : MD5 of this video calculated by the script.

`video_integrity` : `1` if `video_md5_vimeo` and `video_md5_calculated` are equals, else `0`.


## Documentation
https://developer.vimeo.com/api/start


## Inspiration
https://github.com/yeeking/vimeo-account-downloader/blob/master/vimeo_backup.py


## Credits
[Sciences Po - Library](http://www.sciencespo.fr/bibliotheque/en)


## Licenses
[LGPL V3.0](http://www.gnu.org/licenses/lgpl.txt "LGPL V3.0")

[CECILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.html "CECILL-C")