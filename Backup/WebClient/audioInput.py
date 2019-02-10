# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import sys;

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = sys.argv[1]

document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

score = sentiment.score

if score >= -1.0 and score < -0.25:
    print(":(")
if score >= -0.25 and score < 0.25:
    print(":/")
if score >= 0.25 and score <= 1:
    print(":)")
