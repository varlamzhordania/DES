class ShoppingCart {

    constructor() {
        this.cartQuantity = document.querySelector("#shopping-cart-quantity")
        this.shoppingCartTotal = document.querySelector("#shopping-cart-total")
        this.items = [];
    }

    findItemIndexById(id) {
        return this.items.findIndex(item => item.id === id);
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

        this.updateCart();
    }

    removeItem(id) {
        const index = this.findItemIndexById(id);

        if (index !== -1) {
            this.items.splice(index, 1);
            this.updateCart();
        } else {
            console.error("Item not found for removal.");
        }
    }

    decreaseQuantity(id, newQuantity, seat) {
        const index = this.findItemIndexById(id);
        if (index !== -1 && newQuantity >= 0) {
            this.items[index].quantity -= newQuantity
            this.items[index].seats = this.items[index].seats.filter(item => item !== seat)
            this.items = this.items.filter(item => item.quantity > 0);
            this.updateCart();
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

    updateCart() {
        this.displayCart();

        this.cartQuantity.textContent = this.getQuantity()
        this.shoppingCartTotal.textContent = '$' + this.calculateTotal().toFixed(2)
    }

}

export default ShoppingCart