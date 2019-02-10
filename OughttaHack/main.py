# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import io

# [START gae_python37_auth_verify_token]
from flask import Flask, render_template, request, Response, jsonify
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token

firebase_request_adapter = requests.Request()
# [END gae_python37_auth_verify_token]

datastore_client = datastore.Client()

app = Flask(__name__)


def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

# transcribe function
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        return(str(result.alternatives[0].transcript))
# end transcribe

@app.route("/api")
def api(DATAA):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    text = transcribe_file(DATAA)
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    score = sentiment.score
    senti = ""
    print(text)
    if score >= -1.0 and score < -0.25:
        senti = "Bad/Sad"
    if score >= -0.25 and score < 0.25:
        senti = "Neutral"
    if score >= 0.25 and score <= 1:
        senti = "Good/Happy"

    # Score Range 0.25 
    # -1.0 - -0.25 = BAD
    # —0.25 - 0.25 = NEUTRAL
    # 0.25 - 1.0 = GOOG
    data = {'sentiment': senti, "test":text}
    return jsonify(data)



# [START gae_python37_auth_verify_token]
@app.route('/')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

        # Record and fetch the recent times a logged-in user has accessed
        # the site. This is currently shared amongst all users, but will be
        # individualized in a following step.
        store_time(datetime.datetime.now())
        times = fetch_times(10)

    return render_template(
        'index.html',
        user_data=claims, error_message=error_message, times=times)
# [END gae_python37_auth_verify_token]


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
