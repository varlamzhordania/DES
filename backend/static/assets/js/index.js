import ShoppingCart from "./cart.js"

const toasts = document.getElementsByClassName('toast')
const sidebarWrapper = document.querySelector(".sidebar-wrapper")
const mainToggler = document.querySelector("#main-toggler")
const sidebarAside = document.querySelector("#sidebar-aside")
const backdrop = document.createElement("div")
const btnOrders = document.querySelectorAll('.btn-order')


const myCart = new ShoppingCart();
let loadedFood;

let orderModal;
if (document.querySelector("#modal-order")) {
    orderModal = new bootstrap.Modal('#modal-order', {})
}

if (sidebarAside)
    sidebarAside.appendChild(backdrop)
const triggerToast = (item) => {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(item)
    toastBootstrap.show()
}

for (let toast of toasts) {
    triggerToast(toast)
}


const sidebarToggle = (e) => {
    sidebarWrapper.classList.toggle("active")
    if (sidebarWrapper.classList.contains("active")) {
        backdrop.classList.add("backdrop")
    } else {
        backdrop.classList.remove("backdrop")
    }
}
if (mainToggler)
    mainToggler.addEventListener("click", sidebarToggle)

backdrop.addEventListener("click", () => {
    if (sidebarWrapper.classList.contains("active")) {
        sidebarToggle()
    }
})


const getData = async (url) => {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method: "get"
    })
    return await response.json()
}

function setTemplate() {
    const data = this;
    let output = ``;
    let color = 'seat-deactive';

    output += `
      <div class="d-flex flex-column justify-content-center align-items-center">
        <button class="seat seat-lg text-light mb-1 ${color}" data-id="${data.id}">
            ${chairIcon}
        </button>
        <span>${data.name}</span>
       </div>
   `;

    return output;
}

const renderUserSeats = async () => {
    const data = await getData('api/user/');
    const wrapper = document.createElement('div');
    wrapper.classList.add('seat-wrapper');

    const seats = data?.seats;

    if (seats && seats.length > 0) {
        seats.forEach((seat) => {
            const seatElement = setTemplate.apply(seat);
            const elementDiv = document.createElement("div")
            elementDiv.innerHTML = seatElement
            wrapper.appendChild(elementDiv);
        });
    }

    return wrapper;
};


const handleSeatClick = () => {
    document.querySelectorAll(".seat").forEach(seat => {
        seat.addEventListener("click", (e) => {
            let target = e.currentTarget
            const id = target.getAttribute("data-id")
            if (target.classList.contains("seat-deactive")) {
                target.classList.remove("seat-deactive")
                target.classList.add("seat-active")
                myCart.addItem(loadedFood.id, loadedFood.name, 1, loadedFood.price, id)
                return

            }
            if (target.classList.contains("seat-active")) {
                target.classList.remove("seat-active")
                target.classList.add("seat-deactive")
                myCart.decreaseQuantity(loadedFood.id, 1, id)
                return
            }
        })
    })
}


if (btnOrders)
    btnOrders.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const divContent = document.querySelector("#modal-order-content")
            let foodId = e.currentTarget.getAttribute("data-id")
            document.querySelector("#food-id").value = foodId

            orderModal.show()

            const food_data = await getData(`api/food-detail/${foodId}/`)
            loadedFood = food_data
            let img_src = food_data?.thumbnail ?? '/static/assets/image/food-default.jpg'

            const seatsWrapper = await renderUserSeats()
            divContent.innerHTML = `
            <div class="row row-cols-1 row-cols-lg-2">
                <div class="col">
                    <img src="${img_src}" alt="${food_data?.name}" class="card-img rounded" />
                </div>
                <div class="col">
                    <div class="card-body">
                        <h2 class="card-title fw-bold my-3">${food_data?.name}</h2>
                        <h4 class="card-title text-primary my-4">$${food_data?.price}</h4>
                        <p class="card-text my-3">${food_data?.description}</p>
                        <p class="card-text my-3 fw-bold">${food_data?.ingredients}</p>
                        ${seatsWrapper.outerHTML}     
                    </div>
                </div>
            </div>
            `
            handleSeatClick()

        })
    })


const chairIcon = `
<svg width="64" height="64" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="">
    <path fill="currentColor" d="M7.402 4.5C7 5.196 7 6.13 7 8v4.027C7.43 12 7.914 12 8.435 12h7.13c.52 0 1.005 0 1.435.027V8c0-1.87 0-2.804-.402-3.5A3 3 0 0 0 15.5 3.402C14.804 3 13.87 3 12 3s-2.804 0-3.5.402A3 3 0 0 0 7.402 4.5" opacity=".5"/>
    <path fill="currentColor" d="M6.25 15.991c-.502-.02-.806-.088-1.014-.315c-.297-.324-.258-.774-.18-1.675c.055-.65.181-1.088.467-1.415C6.035 12 6.858 12 8.505 12h6.99c1.647 0 2.47 0 2.982.586c.286.326.412.764.468 1.415c.077.9.116 1.351-.181 1.675c-.208.227-.512.295-1.014.315V21a.75.75 0 1 1-1.5 0v-5h-8.5v5a.75.75 0 1 1-1.5 0z"/>
</svg>
`
