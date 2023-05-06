# Youtube API Downloader


* Description

Platform: Python Flask

Release Date: 17.04.2023

This API can download any mp3 file as mono mp3 file


Don't forget to download FFMPEG: https://phoenixnap.com/kb/install-ffmpeg-ubuntu



* API Call

At this time, this API is locally hosted

1. Get the song Youtube URL:

http://localhost:5000/get_link?api_key={your_api_key}&payload={your_payload}

Response format if the link is found:

```
{
    "message":<link>,
    "success":true,
    "video_id":<id>
}
```

The video_id can be used to store uniquely a song.

2. Download directly the mp3 song as mono:

http://localhost:5000/download_mp3?api_key={your_api_key}&payload={your_payload}


3. Download the mp3 file from Youtube URL:

http://localhost:5000/download_mp3_url?api_key={your_api_key}&payload={your_payload}


Both 2 and 3 will send the mp3 as binary file in response.content

The API Key can be stored in .env file of the project. You must create your own. xD



* Used resources

1. https://stackoverflow.com/questions/68230294/how-can-i-play-audio-file-sent-from-flask-send-file

2. https://pythonbasics.org/flask-rest-api/

3. https://chat.openai.com/

