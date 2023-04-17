'''
My personal Youtube API used to play music
for Pico W as a mono mp3 song
'''
import os
import time
import subprocess
import supervisor
from flask import Flask, request, jsonify, send_file
import pytube
from pytube import YouTube
from pydub import AudioSegment

app = Flask(__name__)
try:

    @app.route('/download_mp3', methods=['GET'])
    def download_mp3():
        '''
        Function called to download the mp3
        and convert it in mono
        '''
        payload = request.args.get('payload')
        # First find the url for payload
        try:
            query = f"{payload}"
            results = pytube.Search(query).results
            video = results[0]
            url = video.watch_url
        except pytube.exceptions.RegexMatchError as regex_error:
            return jsonify({'success': False,
                            'message': "Error at converting the payload to link: " + str(regex_error)})
        # Download track using url
        try:
            youtube_music = YouTube(url)
            video = youtube_music.streams.filter(only_audio=True).first()
            destination = '.'
            out_file = video.download(output_path=destination)
            # If the file is not ready
            while True:
                if os.path.exists(out_file) and os.path.getsize(out_file) == video.filesize:
                    break
                time.sleep(1)
            parent_dir = os.getcwd()
            print(parent_dir)
            subprocess.run([
                'ffmpeg',
                '-i', os.path.join(parent_dir, out_file),
                os.path.join(parent_dir, "song_todo.mp3"),
                '-y'
            ], check=True)
            os.remove(out_file)
            try:
                # Transform audio to mono
                song = AudioSegment.from_file("song_todo.mp3", format="mp3")
                # convert to mono
                song_mono = song.set_channels(1)
                # export as mono MP3 file
                song_mono.export("song.mp3", format="mp3")
                os.remove("song_todo.mp3")
                return send_file("song.mp3", mimetype="audio/mp3")
            except IOError as mono_error:
                return jsonify({'success': False,
                                'message': "Error at converting to mono: " + str(mono_error)})
        except pytube.exceptions.VideoUnavailable as download_error:
            return jsonify({'success': False,
                            'message': "Error at downloading: " + str(download_error)})

    app.run()
except Exception as e:
    supervisor.reload()