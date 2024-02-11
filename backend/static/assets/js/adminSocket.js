import {formatDate} from "./utils.js";

class AdminWebSocket {
    constructor(orderListBodyID) {

        this.orderListBody = document.querySelector(orderListBodyID)

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
        this.sendSignal("user_list", {})
        this.sendSignal("order_list", {})
        this.sendSignal("room_list", {})
    }

    onMessage(event) {
        const data = JSON.parse(event.data);
        switch (data?.action) {
            case "user_list" :
                this.updateUsersList(data?.results);
                break
            case "order_list":
                this.updateOrderList(data?.results)
                break
            case "room_list":
                this.updateUsersList(data?.results)
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

    updateRoomList(data) {
        console.log(data)
    }

    updateOrderList(data) {
        this.orderListBody.innerHTML = "";
        const table = document.createElement("table");
        const tableHeader = document.createElement("thead");
        const tableBody = document.createElement("tbody");
        const tableHeaderTr = document.createElement("tr");
        table.classList.add("table", "table-light", "table-hover");
        tableHeader.classList.add("table-dark", "position-sticky", "top-0");

        ["ID", "Table", "Status", "Method", "Payment", "Date"].forEach(headerText => {
            const th = document.createElement("th");
            th.scope = "row";
            th.textContent = headerText;
            tableHeaderTr.appendChild(th);
        });

        data?.forEach(item => {
            const tr = document.createElement("tr");
            tr.style.cursor = "pointer";
            tr.addEventListener("click", () => {
                window.location.href = `/dashboard/orders/detail/${item.id}/`;
            });

            const idCell = document.createElement("th");
            idCell.textContent = `#${item?.id}`;
            tr.appendChild(idCell);

            const userCell = document.createElement("td");
            userCell.textContent = `${item?.user}`;
            tr.appendChild(userCell);

            const statusCell = document.createElement("td");
            statusCell.innerHTML = `<span class="badge bg-primary">${item?.status}</span>`;
            tr.appendChild(statusCell);

            const methodCell = document.createElement("td");
            methodCell.innerHTML = `<span class="badge bg-info">${item?.payment_method}</span>`;
            tr.appendChild(methodCell);

            const paymentCell = document.createElement("td");
            paymentCell.innerHTML = `<span class="badge bg-secondary">${item?.payment_status}</span>`

            tr.appendChild(paymentCell);

            const dateCell = document.createElement("td");
            dateCell.textContent = `${formatDate(item?.create_at)}`;
            tr.appendChild(dateCell);

            tableBody.appendChild(tr);
        });

        tableHeader.appendChild(tableHeaderTr);
        table.appendChild(tableHeader);
        table.appendChild(tableBody);
        this.orderListBody.appendChild(table);
    }

    updateUsersList(data) {
        console.log(data)
    }
}

const adminWebSocket = new AdminWebSocket("#order-list-body",);