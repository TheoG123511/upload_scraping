upload_scraping
==============

> Download video from html page or html iframe. Just need link :)

Installation
--------------

### How to install ?

* get the netu_scraping source code
```sh
$ git clone <upload_scraping repo> <src dir>
```
* into **root directory** 
```sh
$ pip install .
```

Usage
--------------
* get information about url
```sh
$ upload_video_downloader.py a -s <your url> 
$ upload_video_downloader.py about -s <your url>  -v
$ upload_video_downloader.py about -s <your file>
```
* download video from url
```sh
$ upload_video_downloader.py d -s <your url> -o <output_directory>
$ upload_video_downloader.py download -s <your url> -o <output_directory> -v
$ upload_video_downloader.py download -s <your url>
```
* download video from file
```sh
$ upload_video_downloader.py d -s <your file> -o <output_directory>
$ upload_video_downloader.py download -s <your file> -o <output_directory> -v
$ upload_video_downloader.py download -s <your file>
```

Docker
--------------

* Build container **test**
```sh
$ docker-compose -f docker-compose-test.yml up --build -d
```
* Build container **production**
```sh
$ docker-compose up --build -d
```
* Copy file into container
```sh
$ docker cp <file_link.txt> <container_id>:/link.txt
```
* Run download
```sh
$ docker exec -it <container_id> run_app
```


Test
--------------
* test in **local**
```sh
$ py -m unittest discover
$ pytest test
```
* test in **docker**
```sh
$ docker exec -it <container_id> run_test
```

Schema
--------------

![upload scraping package](upload_scraping/src/package_uml.png)


Announcement
--------------
upload_scraping is an experimental project