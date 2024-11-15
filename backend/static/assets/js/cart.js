import {toast} from "./utils.js";

class ShoppingCart {

    constructor() {
        this.cartQuantity = document.querySelector("#shopping-cart-quantity")
        this.shoppingCartTotal = document.querySelector("#shopping-cart-total")
        this.subtotalSpan = document.querySelector("#subtotal")
        this.items = [];
        this.loadFromServer()
    }

    findItemIndexById(id) {
        return this.items.findIndex(item => item.id == id);
    }

    addItem(id, name, quantity, price, seat) {
        const existingIndex = this.findItemIndexById(id);

        if (existingIndex !== -1) {
            this.items[existingIndex].quantity += quantity;
            if (this.items[existingIndex].seats.filter(seatId => seatId === seat).length <= 0) {
                this.items[existingIndex].seats.push(seat)
            }
        } else {
            const newItem = {
                id: id,
                name: name,
                quantity: quantity,
                price: price,
                seats: [seat]
            };
            this.items.push(newItem);
        }


        this.items = this.items.filter(item => item.quantity > 0);
        toast(`${name} added to your cart`, 5000, "success")
        this.updateCart();
        this.updateServer()
    }

    removeItem(id) {
        const index = this.findItemIndexById(id);

        if (index !== -1) {
            const name = this?.items[index]?.name
            this.items.splice(index, 1);
            this.updateCart();
            this.updateServer()
            toast(`${name} deleted from your cart`, 5000, "error")

        } else {
            console.error("Item not found for removal.");
        }
    }

    decreaseQuantity(id, newQuantity, seat, name) {
        const index = this.findItemIndexById(id);
        if (index !== -1 && newQuantity >= 0) {
            this.items[index].quantity -= newQuantity
            this.items[index].seats = this.items[index].seats.filter(item => item !== seat)
            this.items = this.items.filter(item => item.quantity > 0);
            toast(`${name} removed from your cart`, 5000, "error")
            this.updateCart();
            this.updateServer()
        } else {
            console.error("Item not found or invalid quantity for updating.");
        }
    }

    updateQuantity(id, newQuantity) {
        const index = this.findItemIndexById(id);

        if (index !== -1 && newQuantity >= 0) {
            this.items[index].quantity = newQuantity;

            this.items = this.items.filter(item => item.quantity > 0);
            this.updateCart();
            this.updateServer()
        } else {
            console.error("Item not found or invalid quantity for updating.");
        }
    }

    getFoodSeats(index) {
        return this?.items[index]?.seats || []
    }

    getQuantity() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }

    calculateTotal() {
        return this.items.reduce((total, item) => total + item.quantity * item.price, 0);
    }

    displayCart() {
        console.log("Shopping Cart:");
        this.items.forEach((item, index) => {
            console.log(`${index + 1}. ${item.name} - Quantity: ${item.quantity} - Price: ${item.price} , Seats: ${item.seats.join(",")}`);
        });
        console.log(`Total: $${this.calculateTotal().toFixed(2)}`);
    }

    async updateServer() {
        const csrftoken = Cookies.get('csrftoken');

        const prepData = JSON.stringify(this.items)
        const response = await fetch(`/api/cart/`, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": csrftoken,
            },
            method: "post",
            body: prepData
        })
        const data = await response.json()
        if (response.status === 404 && data?.error === "food is not available") {
            this.removeItem(data?.data?.id)
            toast(`unfortunately ${data.data.name} is not available right now!!!`, 5000, "warning")
        }

    }

    async loadFromServer() {
        const response = await fetch(`/api/cart/`, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method: "get",
        })
        const data = await response.json()
        const cartItems = data?.cart_items
        cartItems.forEach(item => {
            const prepItem = {
                id: item?.food?.id,
                name: item?.food?.name,
                quantity: item.quantity,
                price: item?.food?.price,
                seats: item?.seats
            }
            this.items.push(prepItem)
        })
        this.updateCart();
    }

    updateCart() {
        this.displayCart();
        this.cartQuantity.textContent = this.getQuantity();
        this.shoppingCartTotal.textContent = '$' + this.calculateTotal().toFixed(2);
        this.subtotalSpan.textContent = '$' + this.calculateTotal().toFixed(2);

        const copySubtotalSpan = this.subtotalSpan.parentNode.cloneNode(true);
        const parentSubtotalSpan = this.subtotalSpan.parentNode.parentNode;
        parentSubtotalSpan.innerHTML = ``
        parentSubtotalSpan.appendChild(copySubtotalSpan);
        this.items.forEach(item => {
            const div = document.createElement("div");
            div.classList.add("hstack", "justify-content-between", "align-items-center")
            const name = document.createElement("small");
            name.classList.add("text-black-50")
            const value = document.createElement("small");
            value.classList.add("text-black-50")
            name.textContent = `–${item.name}`;
            value.textContent = `$${item.price}x${item.quantity}`

            div.appendChild(name);
            div.appendChild(value);

            parentSubtotalSpan.appendChild(div);
        });


    }


}

export default ShoppingCart