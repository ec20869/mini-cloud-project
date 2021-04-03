# Import the necessary libraries
from flask import Flask, jsonify, json, request
import mysql.connector
import requests
import json
import collections

# Libraries that are no longer needed
#import jwt
#import pandas as pd

app = Flask(__name__)

# This allows for testing when the database is turned off
try:
    # Define the connection parameters for the SQL database
    mydb = mysql.connector.connect(
    host="rds-mysql-musicapp.cthtio1llmic.us-east-1.rds.amazonaws.com",
    user="admin",
    password="music123",
    database="music"
    )
except:
    x=1



@app.route('/')
def api_information():
    # This function returns a HTML page with information on all the other APIs
    return """<html>
<body>
<h1>Music API Service</h1>
<h3>Designed, developed and implemented by Freddie Sauvundra, Tom Doyle and Christa Dobson</h3>
<br></br>
<br></br>
<b>Get all the records</b>
<p>Request type: GET</p>
<p>Path: /records/</p>
<br></br>
<b>Get albums by bandname</b>
<p>Request type: GET</p>
<p>Path: /records/<bandname></p>
<p>Example Path: /records/Radiohead</p>
<br></br>
<b>Get songs by band and album</b>
<p>Request type: GET</p>
<p>Path: /records/<bandname>/<albumtitle></p>
<p>Example Path: /records/Radiohead/TheKingofLimbs</p>
<br></br>
<b>Create a record</b>
<p>Request type: POST</p>
<p>Path: /records/<bandname></p>
<p>Example Path: /records/ColdPlay</p>
<br></br>
<b>Delete a band</b>
<p>Request type: DELETE</p>
<p>Path: /records/delete/<bandname></p>
<p>Example Path: /records/delete/Portishead
<br></br>
</body>
</html>"""


@app.route('/records', methods=['GET'])
def get_all_records():
	return jsonify(all_records)


@app.route('/records/<bandname>', methods=['GET','DELETE'])
def get_albums_by_band(bandname):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404
    else:
        response = [album['title'] for album in albums[0]]
        return jsonify(response), 200
    

@app.route('/records/<bandname>/<albumtitle>', methods=['GET'])
def get_songs_by_band_and_album(bandname, albumtitle):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404      
    else:
        songs = [album['songs'] for album in albums[0] if album['title'] == albumtitle]
        if len(songs)==0:
            return jsonify({'error':'album title not found!'}), 404
        else:
            return jsonify(songs[0]), 200
    

@app.route('/records', methods=['POST'])
def create_a_record():
    if not request.json or not 'name' in request.json:
        return jsonify({'error':'the new record needs to have a band name'}), 400
    new_record = {
        'name': request.json['name'],
        'albums': request.json.get('albums', '')
    }
    all_records.append(new_record)
    return jsonify({'message':'new band created: /records/{}'.format(new_record['name'])}), 201


@app.route('/records/<bandname>', methods=['DELETE'])
def delete_a_band(bandname):
    matching_records = [band for band in all_records if band['name'] == bandname]
    if len(matching_records)==0:
        return jsonify({'error':'band name not found!'}), 404
    all_records.remove(matching_records[0])
    return jsonify({'success': True})


@app.route('/records/<bandname>/search', methods=['GET'])
def search_a_song_by_band(bandname, albumtitle):
    albums = [band['albums'] for band in all_records if band['name'] == bandname]
    if len(albums)==0:
        return jsonify({'error':'band name not found!'}), 404      
    else:
        songs = [album['songs'] for album in albums[0] if album['title'] == albumtitle]
        if len(songs)==0:
            return jsonify({'error':'album title not found!'}), 404
        else:
            return jsonify(songs[0]), 200



if __name__ == '__main__':
	app.run(debug=True)
