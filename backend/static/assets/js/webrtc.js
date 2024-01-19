class Webrtc {
    constructor(localVideoId, videoContainerId, messageListId, messageInputId, btnSendMessageId, btnToggleAudio, btnToggleVideo) {
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

                this.btnToggleAudio.addEventListener('click', (e) => {
                    audioTracks[0].enabled = !audioTracks[0].enabled

                    if (audioTracks[0].enabled)
                        this.btnToggleAudio.innerHTML = 'Audio Mute'
                    else
                        this.btnToggleAudio.innerHTML = 'Audio UnMute'

                })
                this.btnToggleVideo.addEventListener('click', (e) => {
                    videoTracks[0].enabled = !videoTracks[0].enabled

                    if (videoTracks[0].enabled)
                        this.btnToggleVideo.innerHTML = 'Video Off'
                    else
                        this.btnToggleVideo.innerHTML = 'Video On'
                })


            })
            .catch((err) => console.log('Error accessing media devices.', err));
    }

    joinChat(username, usernameInput, joinButton, usernameLabel) {
        if (!username) return;
        this.username = username;

        usernameInput.value = '';
        usernameInput.disabled = true;
        usernameInput.classList.add("visually-hidden");

        joinButton.disabled = true;
        joinButton.classList.add("visually-hidden");

        usernameLabel.innerHTML = username;

        this.setupWebSocket();
    }

    setupWebSocket() {
        let location = window.location;
        let wsStart = location.protocol === 'https:' ? 'wss://' : 'ws://';
        let endpoint = wsStart + location.host + '/stream/';
        this.websocket = new WebSocket(endpoint);

        this.websocket.addEventListener('open', (e) => this.onWebSocketOpen(e));
        this.websocket.addEventListener('message', (e) => this.onWebSocketMessage(e));
        this.websocket.addEventListener('close', (e) => console.log('connection closed'));
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
                delete this.mapPeers[peerUsername];
                if (iceConnectionState !== 'closed') {
                    peer.close();
                }
                this.removeVideo(remoteVideo);
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
                delete this.mapPeers[peerUsername];
                if (iceConnectionState !== 'closed') {
                    peer.close();
                }
                this.removeVideo(remoteVideo);
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
            let videoElement = document.createElement('video');
            videoElement.id = username + '-video';
            videoElement.autoplay = true;
            videoElement.playsInline = true;
            videoElement.classList.add('card-img');

            let cardBody = document.createElement('div');
            cardBody.classList.add('card-body');
            cardBody.appendChild(videoElement);

            let card = document.createElement('div');
            card.classList.add('card');
            card.appendChild(cardBody);

            let colWrapper = document.createElement('div');
            colWrapper.classList.add('col');
            colWrapper.appendChild(card);

            this.videoContainer.appendChild(colWrapper);

            return videoElement;
        } else {
            return document.querySelector(`#${username}-video`).node
        }

    }

    removeVideo(video) {
        let videoWrapper = video.parentNode
        videoWrapper.parentNode.parentNode.parentNode.removeChild(videoWrapper.parentNode.parentNode)
    }

    dcOnMessage(e) {
        let message = e.data;
        let li = document.createElement('li');
        li.appendChild(document.createTextNode(message));
        this.messageList.appendChild(li);
    }

    getDataChannels() {
        return Object.values(this.mapPeers).map((peer) => peer[1]);
    }

    attachEventListeners() {
        this.btnSendMessage.addEventListener('click', () => {
            let message = this.messageInput.value;
            if (message === '') return;

            let li = document.createElement('li');
            li.appendChild(document.createTextNode('Me: ' + message));
            this.messageList.appendChild(li);

            let dataChannels = this.getDataChannels();
            message = this.username + ': ' + message;

            dataChannels.forEach((dc) => dc.send(message));
            this.messageInput.value = '';
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const joinButton = document.querySelector('#btn-join');
    const usernameInput = document.querySelector('#username');
    const usernameLabel = document.querySelector('#username-label');

    const chatApp = new Webrtc('#local-video', '#video-container', '#message-list', '#message-input', '#btn-send-message', '#btn-toggle-audio', '#btn-toggle-video');

    joinButton.addEventListener('click', () => {
        const username = usernameInput.value.trim();
        if (username) {
            chatApp.joinChat(username, usernameInput, joinButton, usernameLabel);
        } else {
            alert("Please enter a username.");
        }
    });

})

