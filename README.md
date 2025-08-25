# Meshtastic Web Chat

**Meshtastic Web Chat** is a lightweight, self-hosted web-based chat system that bridges local network users to the Meshtastic mesh network. It allows anyone connected to your local network to participate in mesh chats through a web browser even if they don't have a Meshtastic device.

By connecting a Meshtastic node via USB to your offline/local server, you can instantly provide seamless browser-based access to the mesh.

<img src="img/img1.png" alt="Meshtastic Web Chat Image 1" width="400" />
<img src="img/img2.png" alt="Meshtastic Web Chat Image 2" width="400" />

## 🚀 Features

* 📡 **Web-Based Mesh Access** – Chat with the Meshtastic mesh using only a web browser.
* 🔌 **No Device Required** – Users on the local network can join the chat without Meshtastic hardware.
* 🌐 **Offline-First** – Fully self-hosted and operates without internet access.
* ⚡ **Real-Time Updates** – Powered by Server-Sent Events (SSE) for instant message delivery.
* 🔧 **Powered by Open Source** – Built with Flask, Meshtastic Python API, and other open-source tools.

## 📦 Requirements

* Python 3.x
* Flask
* Meshtastic Python API (`meshtastic`)
* A Meshtastic node connected via USB

## 🔧 Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/axlixr/meshtastic-web-chat.git
   cd meshtastic-web-chat
   ```

2. **Install Dependencies**
   ```bash
   pip install flask meshtastic pubsub
   ```

3. **Connect Your Meshtastic Node via USB**

4. **Run the Server**
   ```bash
   python app.py
   ```

5. **Access the Chat**
   * On any device connected to the same network, go to:
   ```
   http://[server-ip]:5000
   ```

## ✨ How It Works

* Local users access the chat via a web browser and set a username when they join.
* Messages are sent from the browser to the server using simple POST requests.
* The server automatically tags messages with the user’s chosen username before broadcasting them to the Meshtastic mesh via the USB-connected node.
* Messages sent from the mesh (from other nodes) are displayed in the chat with their node name or ID when available.
* New messages (from both the mesh and local users) are pushed to all connected browsers in real-time using Server-Sent Events (SSE).
* This system ensures that all participants can see who is saying what - both web users and mesh users are clearly identified.

## 📄 License & Attribution

GNU General Public License v3.0

Created by **Axl.**

**Disclaimer:** This is an unofficial project and is not affiliated with or endorsed by the Meshtastic team.

## 🛰️ Acknowledgments

* [Meshtastic](https://meshtastic.org) – Mesh communication platform.
* [Meshtastic Python API](https://github.com/meshtastic/meshtastic-python) – For direct serial communication with the mesh.
* [Flask](https://flask.palletsprojects.com) – Lightweight web server and framework.
