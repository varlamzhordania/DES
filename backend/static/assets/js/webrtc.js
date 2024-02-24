import {toast} from "./utils.js";

class Webrtc {
    constructor(localVideoId, videoContainerId, messageListId, messageInputId, btnSendMessageId, btnToggleAudio, btnToggleVideo, joinButton, disconnectButton) {
        this.localStream = new MediaStream();
        this.mapPeers = {};
        this.websocket = null;
        this.username = null;
        this.rtcConfig = {
            iceServers: [
                {
                    urls: "stun:stun.relay.metered.ca:80",
                },
                {
                    urls: "turn:standard.relay.metered.ca:80",
                    username: "73b45cb344bab8a94d705ab8",
                    credential: "q2vwTsRkc0Qguvpo",
                },
                {
                    urls: "turn:standard.relay.metered.ca:80?transport=tcp",
                    username: "73b45cb344bab8a94d705ab8",
                    credential: "q2vwTsRkc0Qguvpo",
                },
                {
                    urls: "turn:standard.relay.metered.ca:443",
                    username: "73b45cb344bab8a94d705ab8",
                    credential: "q2vwTsRkc0Qguvpo",
                },
                {
                    urls: "turns:standard.relay.metered.ca:443?transport=tcp",
                    username: "73b45cb344bab8a94d705ab8",
                    credential: "q2vwTsRkc0Qguvpo",
                },
            ],
        }

        // DOM elements
        this.localVideo = document.querySelector(localVideoId);
        this.videoContainer = document.querySelector(videoContainerId);
        this.messageList = document.querySelector(messageListId);
        this.messageInput = document.querySelector(messageInputId);
        this.btnSendMessage = document.querySelector(btnSendMessageId);

        this.btnToggleAudio = document.querySelector(btnToggleAudio)
        this.btnToggleVideo = document.querySelector(btnToggleVideo)

        this.btnCall = joinButton
        this.btnDisconnect = disconnectButton

        this.initializeMedia();
        this.attachEventListeners();
    }

    initializeMedia() {
        const constraints = {video: true, audio: true};
        navigator.mediaDevices
            .getUserMedia(constraints)
            .then((stream) => {
                this.localStream = stream;
                this.localVideo.srcObject = this.localStream;
                this.localVideo.muted = true;

                let audioTracks = stream.getAudioTracks()
                let videoTracks = stream.getVideoTracks()

                audioTracks[0].enabled = true
                videoTracks[0].enabled = true

                this.resetToggles()

                this.btnToggleAudio.addEventListener('click', (e) => {
                    audioTracks[0].enabled = !audioTracks[0].enabled

                    if (audioTracks[0].enabled) {
                        this.btnToggleAudio.innerHTML = `<i class="bi bi-mic-fill fs-5"></i>`
                        this.btnToggleAudio.classList.remove("bg-danger")
                        this.btnToggleAudio.classList.add("bg-success")
                    } else {
                        this.btnToggleAudio.innerHTML = `<i class="bi bi-mic-mute-fill fs-5"></i>`
                        this.btnToggleAudio.classList.remove("bg-success")
                        this.btnToggleAudio.classList.add("bg-danger")
                    }

                })

                this.btnToggleVideo.addEventListener('click', (e) => {
                    videoTracks[0].enabled = !videoTracks[0].enabled

                    if (videoTracks[0].enabled) {
                        this.btnToggleVideo.innerHTML = `<i class="bi bi-camera-video-fill fs-5"></i>`
                        this.btnToggleVideo.classList.remove("bg-danger")
                        this.btnToggleVideo.classList.add("bg-success")
                    } else {
                        this.btnToggleVideo.innerHTML = `<i class="bi bi-camera-video-off-fill fs-5"></i>`
                        this.btnToggleVideo.classList.remove("bg-success")
                        this.btnToggleVideo.classList.add("bg-danger")
                    }
                })

                this.btnDisconnect.addEventListener("click", () => {
                    this.disconnectCall()
                })

            })
            .catch((err) => console.log('Error accessing media devices.', err));
    }

    resetToggles() {
        this.btnToggleAudio.innerHTML = `<i class="bi bi-mic-fill fs-5"></i>`
        this.btnToggleAudio.classList.remove("bg-danger")
        this.btnToggleAudio.classList.add("bg-success")
        this.btnToggleVideo.innerHTML = `<i class="bi bi-camera-video-fill fs-5"></i>`
        this.btnToggleVideo.classList.remove("bg-danger")
        this.btnToggleVideo.classList.add("bg-success")
    }

    disconnectCall() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            this.websocket.close();
        }

        Object.keys(this.mapPeers).forEach((key) => {
            const [peer, dc] = this.mapPeers[key]
            if (peer && peer.iceConnectionState !== 'closed') {
                peer.close();
            }
            this.removeVideo(this.getVideoElement(key));
        });

        this.mapPeers = {};

        this.btnCall.classList.remove("visually-hidden");
        this.btnDisconnect.classList.add("visually-hidden");

        this.btnSendMessage.disabled = true
        this.messageInput.disabled = true
        this.messageInput.value = 'make call to use chat'
        this.initializeMedia();
    }

    joinChat(username, room_id) {
        if (!username) return;
        this.username = username;
        this.btnCall.classList.add("visually-hidden");
        this.btnDisconnect.classList.remove("visually-hidden")
        this.btnSendMessage.disabled = false
        this.messageInput.disabled = false
        this.messageInput.value = ''

        this.setupWebSocket(room_id);
    }

    setupWebSocket(id) {
        let location = window.location;
        let endpoint
        let wsStart = location.protocol === 'https:' ? 'wss://' : 'ws://';
        if (id) {
            endpoint = wsStart + location.host + `/ws/stream/${id}/`;
        } else {
            endpoint = wsStart + location.host + '/ws/stream/';
        }
        this.websocket = new WebSocket(endpoint);
        console.log(endpoint)

        this.websocket.addEventListener('open', (e) => this.onWebSocketOpen(e));
        this.websocket.addEventListener('message', (e) => this.onWebSocketMessage(e));
        this.websocket.addEventListener('close', (e) => this.disconnectCall());
        this.websocket.addEventListener('close', (e) => {
            toast("The call has ended.", 5000, "error")
        });
        this.websocket.addEventListener('error', (e) => console.log('Error occurred!'));
    }

    onWebSocketOpen(e) {
        console.log('connection open');
        this.sendSignal('new-peer', {});
    }

    onWebSocketMessage(e) {
        let data = JSON.parse(e.data);
        let action = data.action;

        if (this.username === data.peer) {
            return;
        }

        switch (action) {
            case 'new-peer':
                this.createOffer(data.peer, data.message.receiver_channel_name);
                break;
            case 'new-offer':
                this.createAnswerer(data.message.sdp, data.peer, data.message.receiver_channel_name);
                break;
            case 'new-answer':
                this.handleNewAnswer(data.message.sdp, data.peer);
                break;
            case 'reject-call':
                this.disconnectCall();
                toast("Apologies, we are currently unable to answer your support call. Please try again later.", 5000, 'info');
                break;
            default:
                console.log('Unknown action received:', action);
        }
    }

    sendSignal(action, message) {
        let jsonObject = JSON.stringify({
            peer: this.username,
            action: action,
            message: message,
        });
        this.websocket.send(jsonObject);
    }

    createOffer(peerUsername, channelName) {
        let peer = new RTCPeerConnection(this.rtcConfig);
        this.addLocalTracks(peer);

        let dc = peer.createDataChannel('channel');
        dc.onopen = () => console.log('Connection open');
        dc.onmessage = (e) => this.dcOnMessage(e);

        let remoteVideo = this.createVideo(peerUsername);
        this.setOnTrack(peer, remoteVideo);

        this.mapPeers[peerUsername] = [peer, dc];

        peer.oniceconnectionstatechange = () => {
            let iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === 'failed' || iceConnectionState === "disconnected" || iceConnectionState === "closed") {
                this.disconnectCall()
            }
        }

        peer.onicecandidate = (e) => {
            if (!e.candidate) {
                this.sendSignal('new-offer', {
                    sdp: peer.localDescription,
                    receiver_channel_name: channelName,
                });
            }
        };

        peer.createOffer()
            .then((o) => peer.setLocalDescription(o))
            .then(() => console.log('Local Description set successfully'));
    }

    createAnswerer(offer, peerUsername, receiverChannelName) {

        let peer = new RTCPeerConnection(this.rtcConfig);
        this.addLocalTracks(peer);
        let remoteVideo = this.createVideo(peerUsername);
        this.setOnTrack(peer, remoteVideo);

        peer.ondatachannel = (e) => {
            peer.dc = e.channel;
            peer.dc.onopen = () => console.log('Connection open');
            peer.dc.onmessage = (e) => this.dcOnMessage(e);
            this.mapPeers[peerUsername] = [peer, peer.dc];
        };

        peer.oniceconnectionstatechange = () => {
            let iceConnectionState = peer.iceConnectionState;
            if (iceConnectionState === 'failed' || iceConnectionState === "disconnected" || iceConnectionState === "closed") {
                this.disconnectCall()
            }
        }

        peer.onicecandidate = (e) => {
            if (!e.candidate) {
                this.sendSignal('new-answer', {
                    sdp: peer.localDescription,
                    receiver_channel_name: receiverChannelName,
                });
            }
        };

        peer.setRemoteDescription(new RTCSessionDescription(offer))
            .then(() => peer.createAnswer())
            .then((a) => peer.setLocalDescription(a))
            .then(() => console.log('Answer created'));
    }

    handleNewAnswer(sdp, peerUsername) {
        let peer = this.mapPeers[peerUsername][0];
        peer.setRemoteDescription(new RTCSessionDescription(sdp));
    }

    getVideoElement(username) {
        return document.querySelector(`#${username}-video`).node ? document.querySelector(`#${username}-video`).node : document.querySelector(`#${username}-video`)
    }

    addLocalTracks(peer) {
        this.localStream.getTracks().forEach((track) => {
            peer.addTrack(track, this.localStream);
        });
    }

    setOnTrack(peer, remoteVideo) {
        let remoteStream = new MediaStream();
        remoteVideo.srcObject = remoteStream;
        peer.ontrack = (e) => remoteStream.addTrack(e.track);

    }

    createVideo(username) {
        if (!document.querySelector(`#${username}-video`)) {
            const videoElement = document.createElement('video');
            const div = document.createElement('div');
            videoElement.id = username + '-video';
            videoElement.autoplay = true;
            videoElement.playsInline = true;
            videoElement.classList.add('img-fluid', 'h-100', 'w-100', 'd-block', 'object-fit-cover');
            div.classList.add("w-100", "h-100")
            div.appendChild(videoElement)


            this.videoContainer.appendChild(div);

            return videoElement;
        } else {
            return document.querySelector(`#${username}-video`).node
        }

    }

    removeVideo(video) {
        let videoWrapper = video.parentNode
        videoWrapper.parentNode.removeChild(videoWrapper)
    }

    dcOnMessage(e) {
        let message = e.data;
        let li = document.createElement('li');
        let icon = document.createElement('i');
        let span = document.createElement('span');
        icon.classList.add("bi", "bi-headset", "fs-3")
        icon.style.alignSelf = "end"
        li.classList.add("d-flex", "align-items-center", "justify-content-start", "gap-1", "my-2")
        span.classList.add("bg-white", "text-dark", "p-2", "rounded", "w-auto", "text-break", "shadow-sm")
        span.textContent = message
        li.appendChild(icon);
        li.appendChild(span)
        this.messageList.appendChild(li);
    }

    getDataChannels() {
        return Object.values(this.mapPeers).map((peer) => peer[1]);
    }

    attachEventListeners() {
        // Add click event listener to the button
        this.btnSendMessage.addEventListener('click', () => {
            this.sendMessage();
        });

        // Add keydown event listener to the message input field
        this.messageInput.addEventListener('keydown', (event) => {
            // Check if the pressed key is 'Enter' (key code 13)
            if (event.keyCode === 13 && !event.shiftKey && !event.ctrlKey) {
                event.preventDefault()
                this.sendMessage();
            }
        });
    }

    sendMessage() {
        let message = this.messageInput.value.trim();
        if (message === '') {
            // Handle empty message
            return;
        }

        let li = document.createElement('li');
        let icon = document.createElement('i');
        let span = document.createElement('span');
        icon.classList.add("bi", "bi-person", "fs-3")
        icon.style.alignSelf = "end"
        li.classList.add("d-flex", "align-items-center", "justify-content-start", "gap-1", "my-2")
        span.classList.add("p-2", "rounded", "w-auto", "text-break")
        span.textContent = message
        li.appendChild(icon);
        li.appendChild(span)
        this.messageList.appendChild(li);

        let dataChannels = this.getDataChannels();
        // message = this.username + ': ' + message;

        dataChannels.forEach((dc) => dc.send(message));
        this.messageInput.value = '';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const joinButton = document.querySelector('#btn-join');
    const disconnectButton = document.querySelector('#btn-disconnect');
    const usernameInput = document.querySelector('#username');
    const roomIDInput = document.querySelector('#room_id');

    const chatApp = new Webrtc('#local-video', '#video-container', '#message-list', '#message-input', '#btn-send-message', '#btn-toggle-audio', '#btn-toggle-video', joinButton, disconnectButton);

    joinButton.addEventListener('click', () => {
        const username = usernameInput.value.trim();
        let room_id = null
        if (roomIDInput)
            room_id = roomIDInput.value
        if (username) {
            chatApp.joinChat(username, room_id);
        } else {
            console.log(username)
            alert("Please enter a username.");
        }
    });

})

