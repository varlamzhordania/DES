import ShoppingCart from "./cart.js"

document.addEventListener("DOMContentLoaded", () => {

    const toasts = document.getElementsByClassName('toast')
    const sidebarWrapper = document.querySelector(".sidebar-wrapper")
    const mainToggler = document.querySelector("#main-toggler")
    const sidebarAside = document.querySelector("#sidebar-aside")
    const backdrop = document.createElement("div")
    const foodListContainer = document.querySelector("#food-list")
    const categoryListContainer = document.querySelector("#category-list")
    const shoppingCartBtn = document.querySelector("#shopping-cart-btn")
    const shoppingCartBody = document.querySelector("#shoppingCartBody")
    const myCart = new ShoppingCart();
    const FOOD_LIST = []
    const DEFAULT_FOOD_URL = '/static/assets/image/food-default.jpg'
    const DEFAULT_CATEGORY_URL = 'static/assets/image/category-default.jpg'
    let btnOrders;
    let shoppingCartCanvas;
    let categoryParam
    let loadedFood = {};
    let orderModal;

    const triggerToast = (item) => {
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(item)
        toastBootstrap.show()
    }

    for (let toast of toasts) {
        triggerToast(toast)
    }
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

    if (document.querySelector("#shopping-cart-canvas"))
        shoppingCartCanvas = new bootstrap.Offcanvas('#shopping-cart-canvas')


    if (document.querySelector("#modal-order"))
        orderModal = new bootstrap.Modal('#modal-order', {})

    if (sidebarAside)
        sidebarAside.appendChild(backdrop)


    const updateFoodList = async (category) => {
        let url;
        if (category)
            url = `/api/food-list/?category__slug=${category}`
        else
            url = `/api/food-list/`
        const foodData = await getData(url)
        foodListContainer.innerHTML = ``

        foodData.map(food => {
            FOOD_LIST.push(food)
            let imageSrc = food.thumbnail ?? DEFAULT_FOOD_URL
            foodListContainer.innerHTML += `
            <div class="col">
                    <div class="card card-food h-100 bg-light shadow">
                        <div class="card-img-wrapper">
                             <img src="${imageSrc}" alt="${food.name}" class="card-img"/>
                        </div>
                        <span class="position-absolute fs-3 text-white bg-white bg-opacity-25 px-2 pt-1 rounded"
                              style="left:10px;top:10px">
                            <i class="bi bi-exclamation-circle"></i>
                        </span>
                        <div class="card-body">
                            <h3 class="card-title fw-bold">
                                ${food.name}
                            </h3>
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <h4 class="card-title text-primary fw-normal">${food.price}</h4>
                                <button class="btn btn-sm btn-secondary text-white btn-order" data-id="${food.id}"><i
                                        class="bi bi-cart-plus me-2"></i>ORDER
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `
        })
        btnOrders = document.querySelectorAll('.btn-order')
        addBtnOrderEvent()
    }
    if (foodListContainer)
        updateFoodList(categoryParam)


    const updateCategoryList = async () => {
        const categoryData = await getData('api/category-list/')
        categoryListContainer.innerHTML = ``
        categoryData.map(category => {
            let imageSrc = category.image ?? DEFAULT_CATEGORY_URL
            categoryListContainer.innerHTML += `
            <swiper-slide>
                <div class="card card-category overflow-hidden" data-slug="${category.slug}">                      
                    <img src="${imageSrc}" alt="${category.name}" class="card-img h-100 object-fit-cover"/>      
                    <div class="card-img-overlay d-flex align-items-center">
                        <h3 class="card-title text-light position-relative d-block z-1 mb-0">
                            ${category.name}
                        </h3>
                    </div>
                </div>
            </swiper-slide>
            `
        })

        document.querySelectorAll(".card-category").forEach(category => {
            category.addEventListener("click", (e) => {
                categoryParam = e.currentTarget.getAttribute("data-slug")
                foodListContainer.innerHTML = loader
                updateFoodList(categoryParam)
            })
        })

        Object.assign(categoryListContainer, {
            spaceBetween: 15,
            slidesPerView: 2,
            scrollbar: true,
            grid: {
                rows: 2,
            },
            breakpoints: {
                640: {
                    slidesPerView: 3,
                    spaceBetween: 30,
                    scrollbar: false,
                },
                768: {
                    slidesPerView: 3,
                },
                1024: {
                    slidesPerView: 4,
                },
            },
        });
        categoryListContainer.initialize();

    }
    if (categoryListContainer)
        updateCategoryList()

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

    function checkoutTemplate() {
        const data = this
        let imgSrc = data.thumbnail ?? DEFAULT_FOOD_URL
        let output = `
        <li class="row row-cols-3 g-1 gap-0 my-2 border-bottom py-3">
            <div class="col col-2">
                <img src="${imgSrc}" alt="${data.name}" class="card-img rounded">
            </div>
            <div class="col col-9 ps-2">
                <h4>${data.name}</h4>
                <span class="text-primary">$${Number(data.price).toFixed(2)}</span>
            </div>
            <div class="col-1 align-self-center">
                <button class="btn text-dark float-end">
                    <i class="bi bi-x-lg "></i>
                </button>
            </div>
        </li>
        `

        return output
    }

    function seatTemplate() {
        const seat = this;
        let output = ``;
        let foodIndex = myCart.findItemIndexById(seat.food_id)
        let color = foodIndex !== -1 ? myCart.getFoodSeats(foodIndex).includes(seat.id) ? 'seat-active' : 'seat-deactive' : 'seat-deactive';

        output += `
      <div class="d-flex flex-column justify-content-center align-items-center">
        <button class="seat seat-lg text-light mb-1 ${color}" data-id="${seat.id}">
            ${chairIcon}
        </button>
        <span>${seat.name}</span>
       </div>
   `;

        return output;
    }

    const renderUserSeats = async (foodId) => {
        const data = await getData('api/user/');
        const wrapper = document.createElement('div');
        wrapper.classList.add('seat-wrapper');

        const seats = data?.seats;


        if (seats && seats.length > 0) {
            seats.forEach((seat) => {
                seat["food_id"] = foodId
                const seatElement = seatTemplate.apply(seat);
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
                const id = Number(target.getAttribute("data-id"))
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
    const addBtnOrderEvent = () => {
        btnOrders.forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const divContent = document.querySelector("#modal-order-content")
                let foodId = e.currentTarget.getAttribute("data-id")
                document.querySelector("#food-id").value = foodId

                orderModal.show()

                const food_data = await getData(`api/food-detail/${foodId}/`)
                loadedFood = food_data
                let img_src = food_data?.thumbnail ?? DEFAULT_FOOD_URL

                const seatsWrapper = await renderUserSeats(food_data.id)
                divContent.innerHTML = `
                <div class="row row-cols-1 row-cols-lg-2">
                    <div class="col">
                        <img src="${img_src}" alt="${food_data?.name}" class="card-img rounded" />
                    </div>
                    <div class="col">
                        <div class="card-body h-100 d-flex flex-column ">
                        <div>
                            <h2 class="card-title fw-bold my-3">${food_data?.name}</h2>
                            <h4 class="card-title text-primary my-4">$${food_data?.price}</h4>
                        </div>
                        <div class="mb-auto">
                            <p class="card-text my-3">${food_data?.description}</p>
                            <p class="card-text my-3 fw-bold">${food_data?.ingredients}</p>
                        ${seatsWrapper.outerHTML}  
                        </div>
                        <div class="d-flex justify-content-start align-items-center align-self-end w-100 gap-2">
                            <button type="button" class="btn btn-lg  btn-dark w-75" onclick="openShoppingCartInModal()"><i class="bi bi-cart mx-2"></i> Order List</button>   
                            <button type="button" class="btn btn-lg  btn-outline-dark w-25" data-bs-dismiss="modal" aria-label="Close">Close</button> 
                        </div>                        
                          
                        </div>
                    </div>
                </div>
            `
                handleSeatClick()

            })
        })
    }

    const loadShoppingCartEvent = () => {

        shoppingCartCanvas.show()
        const ulElement = document.createElement("ul")
        ulElement.classList.add("list-unstyled","overflow-y-auto","overflow-x-hidden")
        myCart.items.forEach(item => {
            const fullData = FOOD_LIST.filter(food_item => food_item.id == item.id)[0]
            ulElement.innerHTML += checkoutTemplate.apply(fullData)
        })
        shoppingCartBody.innerHTML = ''
        shoppingCartBody.appendChild(ulElement)

    }

    window.openShoppingCartInModal =() => {
        orderModal.hide()
        loadShoppingCartEvent()
    }

    shoppingCartBtn.addEventListener("click", loadShoppingCartEvent)


})

const loader = `
<div class="d-flex justify-content-center align-items-center my-2 gap-2">
    <div class="spinner-grow text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    <div class="spinner-grow text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    <div class="spinner-grow text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
</div>
`

const chairIcon = `
<svg width="64" height="64" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="">
    <path fill="currentColor" d="M7.402 4.5C7 5.196 7 6.13 7 8v4.027C7.43 12 7.914 12 8.435 12h7.13c.52 0 1.005 0 1.435.027V8c0-1.87 0-2.804-.402-3.5A3 3 0 0 0 15.5 3.402C14.804 3 13.87 3 12 3s-2.804 0-3.5.402A3 3 0 0 0 7.402 4.5" opacity=".5"/>
    <path fill="currentColor" d="M6.25 15.991c-.502-.02-.806-.088-1.014-.315c-.297-.324-.258-.774-.18-1.675c.055-.65.181-1.088.467-1.415C6.035 12 6.858 12 8.505 12h6.99c1.647 0 2.47 0 2.982.586c.286.326.412.764.468 1.415c.077.9.116 1.351-.181 1.675c-.208.227-.512.295-1.014.315V21a.75.75 0 1 1-1.5 0v-5h-8.5v5a.75.75 0 1 1-1.5 0z"/>
</svg>
`