import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from api.events.boot import Boot
from api.events.config import Config

# app.add_event_handler("startup", Boot.booting(app))
conf = Config.load()
os.environ['SECRET'] = conf['security']['secret']

app.state.config = conf
app.state.author = 'riza masykur'
# app.state.mongo = await connect_mongo_1(conf)
# app.state.pubsub = PubSub(conf['gcp_pubsub'])

s = Boot.booting(app)
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_read_sandbox():
    response = client.get("/s")
    assert response.status_code == 200
    assert response.json() == {"status": "riza masykur", "org": "aimi"}
