# Youtube API Downloader

* Description

Platform: Python Flask
Release Date: 17.04.2023
This API can downlaod any mp3 file as mono mp3 file

Don't forget to download FFMPEG: https://phoenixnap.com/kb/install-ffmpeg-ubuntu


* API Call

At this time, this API is locally hosted

Download directly the mp3 song as mono:

http://localhost:5000/download_mp3?api_key={your_api_key}&payload={your_payload}


Get the song Youtube URL:

http://localhost:5000/get_link?api_key={your_api_key}&payload={your_payload}


Download the mp3 file from Youtube URL:

http://localhost:5000/download_mp3_url?api_key={your_api_key}&payload={your_payload}



The API Key can be stored in .env file of the project. You must create your own. xD


* Used resources
1. https://stackoverflow.com/questions/68230294/how-can-i-play-audio-file-sent-from-flask-send-file
2. https://pythonbasics.org/flask-rest-api/
3. https://chat.openai.com/
