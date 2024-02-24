import {formatDate} from "./utils.js";

class AdminWebSocket {
    constructor(orderListBodyID, roomListBodyID) {

        this.orderListBody = document.querySelector(orderListBodyID)
        this.roomListBody = document.querySelector(roomListBodyID)
        this.connect()
    }

    connect() {
        const location = window.location;
        this.wsStart = location.protocol === 'https:' ? 'wss://' : 'ws://';
        this.endpoint = this.wsStart + location.host + '/ws/admin/';
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
                this.updateRoomList(data?.results)
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
        const COLORS = ["var(--bs-primary)", "var(--bs-secondary)", "var(--bs-success)", "var(--bs-danger)", "var(--bs-warning)", "var(--bs-info)"];


        this.roomListBody.innerHTML = "";
        const ul = document.createElement("ul")
        ul.classList.add("list-unstyled")
        const newData = data.filter(item => item.is_busy === false)
        if (newData.length > 0) {
            newData.forEach(item => {
                const index = Math.floor(Math.random() * COLORS.length);
                const li = document.createElement("li")
                li.classList.add("border", "border-1")
                li.style.backgroundColor = "var(--bs-gray-100)"
                li.style.borderColor = "var(--bs-gray-200)"
                li.innerHTML = `
            <div class="hstack gap-3">
                <span class="avatar avatar-md text-white" style="background-color: ${COLORS[index]};outline-color: ${COLORS[index]}">
                    ${item.user.username.substring(0, 1).toUpperCase()} ${item.user.username.substring(item.user.username.length - 1, item.user.username.length).toUpperCase()}
                </span>
                <div>
                    <div class="mb-1 fs-5 text-uppercase">${item.user.username}</div>
                    <div class="fs-6">${item.user.customer_name}</div>
                </div>
            </div>
            <div class="hstack gap-2">
                <button class="btn call-btn rounded-circle bg-info text-white shadow fs-5 bounce-animation" style="height: 45px;width: 45px" data-id="${item.id}"><i class="bi-telephone-forward-fill"></i></button>
                <button class="btn reject-btn rounded-circle bg-danger text-white shadow fs-5" style="height: 45px;width: 45px" data-id="${item.id}"><i class="bi-telephone-x-fill"></i></button>
            </div>
            `
                ul.appendChild(li)
            })
        } else {
            const li = document.createElement("li")
            li.classList.add("border", "border-1", "text-center")
            li.style.backgroundColor = "var(--bs-gray-100)"
            li.style.borderColor = "var(--bs-gray-200)"
            li.style.justifyContent = "center"
            li.innerHTML = "<span class='fs-5 fw-bold text-uppercase'>No Support Request</span>"

            ul.appendChild(li)
        }

        this.roomListBody.appendChild(ul)

        document.querySelectorAll(".call-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const id = e.currentTarget.getAttribute("data-id")
                window.open(`/dashboard/support/${id}/`, '_blank');
            })
        })

        document.querySelectorAll(".reject-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const id = e.currentTarget.getAttribute("data-id")
                this.sendSignal("reject_call", {"id": id})
            })
        })
    }

    updateOrderList(data) {
        this.orderListBody.innerHTML = "";
        const table = document.createElement("table");
        const tableHeader = document.createElement("thead");
        const tableBody = document.createElement("tbody");
        const tableHeaderTr = document.createElement("tr");
        table.classList.add("table", "table-hover");
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
                        window.location.href = `/dashboard/orders/${item.id}/`;
                    }
                )
                ;

                const idCell = document.createElement("th");
                idCell.textContent = `#${item?.id}`;
                tr.appendChild(idCell);

                const userCell = document.createElement("td");
                userCell.textContent = `${item?.user}`;
                tr.appendChild(userCell);

                const statusCell = document.createElement("td");
                statusCell.innerHTML = `<span >${item?.status}</span>`;
                tr.appendChild(statusCell);

                const methodCell = document.createElement("td");
                methodCell.innerHTML = `<span >${item?.payment_method}</span>`;
                tr.appendChild(methodCell);

                const paymentCell = document.createElement("td");
                paymentCell.innerHTML = `<span >${item?.payment_status}</span>`

                tr.appendChild(paymentCell);

                const dateCell = document.createElement("td");
                dateCell.textContent = `${formatDate(item?.create_at)}`;
                tr.appendChild(dateCell);

                tableBody.appendChild(tr);
            }
        )
        ;

        tableHeader
            .appendChild(tableHeaderTr);

        table
            .appendChild(tableHeader);

        table
            .appendChild(tableBody);

        this
            .orderListBody
            .appendChild(table);
    }

    updateUsersList(data) {
        console.log(data)
    }
}

const adminWebSocket = new AdminWebSocket("#order-list-body", "#room-list-body");