'''
My personal Youtube API used to play music
for Pico W as a mono mp3 song
'''
import os
import time
import subprocess
import importlib
import sys
from youtube_dl import YoutubeDL
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
import pytube
from pytube import YouTube
from pydub import AudioSegment

load_dotenv()

api_key = os.environ.get("API_KEY")
app = Flask(__name__)
try:
    @app.route('/get_link', methods=['GET'])
    def get_link():
        '''
        Get youtube link from payload
        '''
        # Secure the connection with api_key
        provided_api_key = request.args.get('api_key')
        if provided_api_key != api_key:
            return jsonify({'error': 'Invalid API key'})

        # First find the url for payload
        try:
            payload = request.args.get('payload')
            query = f"{payload}"
            results = pytube.Search(query).results
            indice = 0
            while 'reelShelfRenderer' in results[indice].video_details:
                indice += 1
                
            video = results[indice]
            url = video.watch_url
            # Extract de id from the url
            video_id = url.split("v=")[1]
            return jsonify({'success': True,
                'message': url,
                'video_id': video_id})
        except pytube.exceptions.RegexMatchError as regex_error:
            return jsonify({'success': False,
                            'message': "Error at converting the payload to link: "
                            + str(regex_error)})
        
    @app.route('/download_mp3_url', methods=['GET'])
    def download_mp3_url():
        '''
        Function called to download the mp3
        from specific URL
        and convert it in mono
        '''
        # Secure the connection with api_key
        provided_api_key = request.args.get('api_key')
        if provided_api_key != api_key:
            return jsonify({'error': 'Invalid API key'})
        # Get the url as payload
        try:
            url = request.args.get('payload')
            youtube_music = YouTube(url)
            try:
                while 'lengthSeconds' not in youtube_music.vid_info.get('videoDetails', {}):
                    youtube_music = YouTube(url)
                duration_secs = int(youtube_music.vid_info['videoDetails']['lengthSeconds'])
                if duration_secs > 360:
                        return jsonify({'error': 'Video duration is too long'})
            except pytube.exceptions.RegexMatchError as regex_error:
                return jsonify({'error': 'Error on getting the length'})
            # Download the song
            video = youtube_music.streams.filter(only_audio=True).first()
            destination = '.'
            out_file = video.download(output_path=destination)
            # Check the duration to be lesser than 6 minutes
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
                #song_mono = song_mono.set_frame_rate(32000)

                # export as mono MP3 file
                song_mono.export("song.mp3", format="mp3")
                os.remove("song_todo.mp3")
                return send_file("song.mp3", mimetype="audio/mp3")
            except IOError as mono_exception:
                return jsonify({'success': False,
                                'message': "Error at converting to mono: " + str(mono_exception)})
        except pytube.exceptions.RegexMatchError as regex_error:
            return jsonify({'success': False,
                            'message': "Error at downloading from given url"
                            + str(regex_error)})
        
    @app.route('/download_mp3', methods=['GET'])
    def download_mp3():
        '''
        Function called to download the mp3
        and convert it in mono
        '''
        # Secure the connection with api_key
        provided_api_key = request.args.get('api_key')
        if provided_api_key != api_key:
            return jsonify({'error': 'Invalid API key'})
        # First find the url for payload
        try:
            payload = request.args.get('payload')
            query = f"{payload}"
            results = pytube.Search(query).results
            video = results[0]
            url = video.watch_url
        except pytube.exceptions.RegexMatchError as regex_error:
            return jsonify({'success': False,
                            'message': "Error at converting the payload to link: "
                            + str(regex_error)})
        # Download track using url
        try:
            youtube_music = YouTube(url)
            try:
                # Check the duration to be lower than 6 minutes
                while 'lengthSeconds' not in youtube_music.vid_info.get('videoDetails', {}):
                    youtube_music = YouTube(url)
                duration_secs = int(youtube_music.vid_info['videoDetails']['lengthSeconds'])
                if duration_secs > 360:
                        return jsonify({'error': 'Video duration is too long'})
            except pytube.exceptions.RegexMatchError as regex_error:
                return jsonify({'error': 'Error on getting the length'})
            # Download the song
            video = youtube_music.streams.filter(only_audio=True).first()
            destination = '.'
            out_file = video.download(output_path=destination)
            # Check the duration to be lesser than 6 minutes
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
                # song_mono = song_mono.set_frame_rate(32000)
                # export as mono MP3 file
                song_mono.export("song.mp3", format="mp3")
                os.remove("song_todo.mp3")
                return send_file("song.mp3", mimetype="audio/mp3")
            except IOError as mono_exception:
                return jsonify({'success': False,
                                'message': "Error at converting to mono: " + str(mono_exception)})
        except pytube.exceptions.VideoUnavailable as download_exception:
            return jsonify({'success': False,
                            'message': "Error at downloading: " + str(download_exception)})

    app.run(host='0.0.0.0' , port=5000)
except OSError as app_exception:
    importlib.reload(sys)
