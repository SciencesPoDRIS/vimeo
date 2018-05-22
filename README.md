# Vimeo
Collect metadata and download videos from multiple [Vimeo](https://vimeo.com/) accounts.


## Dependencies

[PyVimeo lib](https://github.com/vimeo/vimeo.py)


## Install

### Code part
Clone the Github project

`> git clone https://github.com/SciencesPoDRIS/vimeo.git`

Go to the freshly created folder

`> cd vimeo`

Create a dedicated virtualenv

`> mkvirtualenv vimeo`

Install dependencies

`> pip install -r requirements.txt`

Copy the default conf file

`> cp conf.default.json conf.json`

### Configuration part

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

### Run script to download videos and metadata
`> workon vimeo`

`> python script.py`

The output will be 2 folders `vimeo_videos` and `vimeo_metadata`. `vimeo_videos` contains all the downloaded videos whose names are Vimeo identifier and format is MP4. `vimeo_metadata` contains all the downloaded metadata whose names are Vimeo identifier and format is JSON.


### Run script to check the quality
`> workon vimeo`

`> python check.py`

The output will be a file named "check_videos.csv" directly in the project folder.

`id` : Unique Vimeo identifier of the video.

`name` : Title of the video from Vimeo.

`url` : Url of the video from Vimeo.

`account` : Name of the user account that uploaded the video from the conf file.

`video_downloaded` : `1` if the video has been downloaded, else `0`.

`metadata_downloaded` : `1` if the metadata file has been dowloaed, else `0`.

`video_md5_vimeo` : MD5 of this video according to Vimeo.

`video_md5_calculated` : MD5 of this video calculated by the script.

`video_integrity` : `1` if `video_md5_vimeo` and `video_md5_calculated` are equals, else `0`. So `1` means that the video file has been correctly downloaded.


## FAQ

### How to set my account to be downloaded ?

* Open the conf.json file.
* Copy / paste an authentifications object.
* And fill it as explain [here](#configuration-part).


## Unseful links

[Vimeo API](https://developer.vimeo.com/api/start)

[Inspiring project](https://github.com/yeeking/vimeo-account-downloader)


## Credits
[Sciences Po - Library](http://www.sciencespo.fr/bibliotheque/en)


## Licenses
[LGPL V3.0](http://www.gnu.org/licenses/lgpl.txt "LGPL V3.0")

[CECILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.html "CECILL-C")