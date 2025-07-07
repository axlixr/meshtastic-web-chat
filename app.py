from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Response
from meshtastic.serial_interface import SerialInterface
from pubsub import pub
import re
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

chat_messages = []
clients = []

interface = SerialInterface()

def clean_username(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '', name)[:20]

@app.route('/set_username', methods=['GET', 'POST'])
def set_username():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        username = clean_username(username)
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('set_username.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('set_username'))

    username = session['username']

    if request.method == 'POST':
        msg = request.form.get('message', '').strip()
        if msg:
            try:
                full_message = f"{username}: {msg}"
                interface.sendText(full_message)
                chat_messages.append(full_message)
                if len(chat_messages) > 100:
                    chat_messages.pop(0)
                broadcast_message(full_message)
            except Exception as e:
                print(f"Error sending message: {e}")
        return redirect(url_for('index'))

    return render_template('index_sse.html', username=username)

@app.route('/stream')
def stream():
    def event_stream():
        messages = chat_messages[:]
        last_index = len(messages)
        while True:
            if len(chat_messages) > last_index:
                new_messages = chat_messages[last_index:]
                last_index = len(chat_messages)
                for msg in new_messages:
                    yield f'data: {msg}\n\n'
            time.sleep(0.5)

    return Response(event_stream(), mimetype="text/event-stream")

def broadcast_message(message):
    # In SSE, this is just appending to the list. 
    # Connected clients pick up the new messages via stream.
    pass  # We don't need explicit broadcasting with this SSE loop

def on_receive(packet, interface):
    try:
        decoded = packet.get('decoded')
        from_node_id = packet.get('from')
        node_name = None

        if from_node_id is not None:
            node = interface.nodes.get(from_node_id)
            if node:
                node_name = node.get('user', {}).get('short_name')

        if decoded and 'payload' in decoded:
            payload = decoded['payload']
            try:
                message = payload.decode('utf-8').strip()
                if all(32 <= ord(c) <= 126 or c in '\r\n\t' for c in message):
                    display_name = node_name if node_name else f"Node {from_node_id}"
                    print(f"Received from {display_name}: {message}")
                    full_message = f"{display_name}: {message}"
                    chat_messages.append(full_message)
                    if len(chat_messages) > 100:
                        chat_messages.pop(0)
            except UnicodeDecodeError:
                pass
    except Exception as e:
        print(f"Error processing packet: {e}")

pub.subscribe(on_receive, "meshtastic.receive")

if __name__ == '__main__':
    print("Starting Meshtastic Web Chat Server with SSE...")
    app.run(host='0.0.0.0', port=5000, threaded=True)
