from email.policy import HTTP
from typing import Any, Coroutine
from sanic import Sanic, Request, response 
from sanic.response import HTTPResponse
from cryptography.fernet import Fernet
from sanic.server.websockets.impl import WebsocketImplProtocol

import rsa

app = Sanic("app")
app.config.OAS = False

actual_messages = []
users = {}
key = Fernet.generate_key()


@app.route('/talk', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    actual_messages.append(request.form["text"][0])
    return response.json({"status": "ok"})


@app.route('/update', methods=["GET", "POST"])
async def talking(request: Request) -> HTTPResponse:
    return response.json({"status": actual_messages, "users_in_chat": list(users.keys())})


@app.route('/get_key', methods=['GET', 'POST'])
async def get_key(request: Request) -> HTTPResponse:
    
    pubkey = rsa.PublicKey.load_pkcs1(request.form['pubkey'][0])
    data = rsa.encrypt(key, pubkey)
    
    if request.ip not in users:
        users[request.form['username'][0]] = key
    
    return response.raw(data)