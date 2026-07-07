from google import genai
client = genai.Client(vertexai=True, project='a4701101-u3666733-1782979541', location='us-central1')
for m in client.models.list():
    print(m.name)