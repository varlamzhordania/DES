class AdminWebSocket {
    constructor() {
        this.connect()
    }

    connect() {
        const location = window.location;
        this.wsStart = location.protocol === 'https:' ? 'wss://' : 'ws://';
        this.endpoint = this.wsStart + location.host + '/admin/';
        this.socket = new WebSocket(this.endpoint);

        this.socket.onopen = this.onOpen.bind(this);
        this.socket.onmessage = this.onMessage.bind(this);
        this.socket.onclose = this.onClose.bind(this);
    }

    onOpen(event) {
        console.log('WebSocket connection opened:', event);
        this.sendSignal("user_list", {})
        this.sendSignal("order_list", {})
    }

    onMessage(event) {
        const data = JSON.parse(event.data);
        switch (data?.action) {
            case "user_list" :
                this.updateUsersList(data?.users);
                break
            case "order_list":
                console.log(data?.orders)
                break
            default:
                break
        }
    }

    onClose(event) {
        console.log('WebSocket connection closed:', event);
        setTimeout(() => {
            this.connect();
        }, 5000);
    }


    sendSignal(action, message) {
        let jsonObject = JSON.stringify({
            action: action,
            message: message,
        });
        this.socket.send(jsonObject);
    }

    updateUsersList(users) {
        console.log(users)
    }
}

const adminWebSocket = new AdminWebSocket();