import ShoppingCart from "./cart.js"
import {EXTRA_LIST, FOOD_LIST, TIP_LIST} from "./constant.js";


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
    const btnCheckout = document.querySelector("#btn-checkout")
    const searchInput = document.querySelector("#search-input")
    const minSearchLength = 3;
    const myCart = new ShoppingCart();
    let abortController = new AbortController();
    const DEFAULT_FOOD_URL = '/static/assets/image/food-default.jpg'
    const DEFAULT_CATEGORY_URL = 'static/assets/image/category-default.jpg'
    let btnOrders;
    let shoppingCartCanvas;
    let categoryParam
    let loadedFood = {};
    let extraSelected = []
    let tipSelected = {}
    let orderModal;
    let debounceTimer;

    const triggerToast = (item) => {
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(item)
        toastBootstrap.show()
    }

    for (let toast of toasts) {
        triggerToast(toast)
    }
    const getData = async (url, signal = abortController.signal) => {
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method: "get",
            signal: signal
        })
        return await response.json()
    }

    if (document.querySelector("#shopping-cart-canvas"))
        shoppingCartCanvas = new bootstrap.Offcanvas('#shopping-cart-canvas')


    if (searchInput) {
        searchInput.addEventListener("input", async (e) => {
            const searchTerm = e.currentTarget.value;

            // Check if the search term meets the minimum length requirement
            if (searchTerm.length < minSearchLength) {
                abortController.abort();
                updateFoodListUI(FOOD_LIST)
                return;
            }

            abortController.abort();
            abortController = new AbortController()


            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(async () => {

                const encodedSearchTerm = encodeURIComponent(searchTerm);
                const url = `/api/food-list/?search=${encodedSearchTerm}`;
                const foodData = await getData(url);
                updateFoodListUI(foodData);
            }, 300);

        });
    }

    const handleExtrasAmount = () => {
        return extraSelected.reduce((total, item) => parseFloat(item.price) + total, parseFloat('0.00'))
    }
    const handleTotalAmount = () => {
        const extraAmount = handleExtrasAmount()
        const tipAmount = tipSelected.amount || 0
        const total = myCart.calculateTotal() + extraAmount + tipAmount
        document.querySelector("#total-amount").textContent = '$' + total.toFixed(2)
        return total
    }


    if (btnCheckout)
        btnCheckout.addEventListener("click", async () => {
            const targetModal = new bootstrap.Modal("#modal-checkout", {})
            targetModal.show()

            const extras = await getData(`/api/extra-list/`)
            const tips = await getData(`/api/tip-list/`)

            const extrasDiv = targetModal._element.querySelector("#extras")
            const tipsDiv = targetModal._element.querySelector("#tips")
            handleTotalAmount()

            extrasDiv.innerHTML = ``
            tipsDiv.innerHTML = ``

            extras.forEach(extra => {
                EXTRA_LIST.push(extra)

                extrasDiv.innerHTML += `
                   <div class="form-check form-check-inline form-check-extra">
                      <input class="form-check-input extra-checkbox" type="checkbox" name="extras" id="extra-checkbox-${extra.id}" data-price="${extra.price}" value="${extra.id}">
                        <label class="form-check-label" for="extra-checkbox-${extra.id}">
                            ${extra.name} 
                            <small class="fw-bold">
                            ($${extra.price})
                            </small>
                        </label>
                   </div>
                `
            })

            tips.forEach(tip => {
                TIP_LIST.push(tip)
                tipsDiv.innerHTML += `
                    <div>
                        <input type="radio" class="btn-check tips-radio" name="tips" id="tip-${tip.id}" data-amount="${tip.amount}" autocomplete="off" value="${tip.id}">
                        <label class="btn btn-outline-dark" for="tip-${tip.id}" style="--bs-btn-active-color: #fff;">${tip.name} <small class="fw-bold">($${tip.amount})</small></label>
                    </div>
                `
            })

            document.querySelectorAll(".extra-checkbox").forEach(checkbox => {
                checkbox.addEventListener("change", (e) => {
                    if (e.target.checked) {
                        let price = e.target.getAttribute("data-price")
                        extraSelected.push({"id": e.target.value, "price": parseFloat(price)})
                        document.querySelector("#extras-amount").textContent = '$' + handleExtrasAmount().toFixed(2)
                    } else {
                        extraSelected = extraSelected.filter(ex => ex.id !== e.target.value)
                        document.querySelector("#extras-amount").textContent = '$' + handleExtrasAmount().toFixed(2)
                    }
                    handleTotalAmount()
                })
            })
            document.querySelectorAll(".tips-radio").forEach(radio => {
                radio.addEventListener("click", (e) => {
                    let amount = parseFloat(e.target.getAttribute("data-amount"))
                    tipSelected = {"id": e.target.value, "amount": amount}
                    document.querySelector("#tip-amount").textContent = '$' + amount
                    handleTotalAmount()
                })
            })


        })

    if (document.querySelector("#modal-order"))
        orderModal = new bootstrap.Modal('#modal-order', {})

    if (sidebarAside)
        sidebarAside.appendChild(backdrop)


    const updateFoodListUI = (foodData, update = false) => {
        foodListContainer.innerHTML = "";

        if (foodData.length <= 0) {
            foodListContainer.classList.add("justify-content-center");
            foodListContainer.innerHTML = `
            <div class="col-12">
                <div class="card bg-transparent border-0">
                    <div class="card-body d-grid text-center">
                        <i class="bi bi-search display-1"></i>
                        <p class="text-black card-text">Could not find any food</p>
                    </div>
                </div>
            </div>
            `;
        } else {
            foodListContainer.classList.remove("justify-content-center");
            foodData.map(food => {
                if (update) {
                    const existsInList = FOOD_LIST.some(item => item.id === food.id);

                    if (!existsInList) {
                        FOOD_LIST.push(food);
                    }
                }
                let imageSrc = food.thumbnail ?? DEFAULT_FOOD_URL
                foodListContainer.innerHTML += `
                <div class="col">
                    <div class="card card-food h-100 bg-light shadow">
                        <div class="row g-0">
                            <div class="col-4 col-md-12">
                                <div class="card-img-wrapper">
                                     <img src="${imageSrc}" alt="${food.name}" class="card-img"/>
                                </div>
                            </div>
                            <div class="col-8 col-md-12">
                                <div class="card-body pb-0">
                                    <h3 class="card-title fw-bold">
                                        ${food.name}
                                    </h3>
                                </div>
                                <div class="card-footer bg-transparent border-0 d-md-flex d-grid justify-content-md-between align-items-center">     
                                    <h4 class="card-title text-primary fw-normal">$${food.price}</h4>
                                    <button class="btn btn-sm btn-secondary text-white btn-order" data-id="${food.id}">
                                        <i class="bi bi-cart-plus me-2"></i>
                                        ORDER
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            })
            btnOrders = document.querySelectorAll('.btn-order');
            addBtnOrderEvent();
            if (update) {
                localStorage.setItem("FOOD_LIST", JSON.stringify(FOOD_LIST))
            }
        }
    };
    const updateFoodList = async (category) => {
        let url;
        if (category)
            url = `/api/food-list/?category__slug=${category}`
        else
            url = `/api/food-list/`
        const foodData = await getData(url)
        updateFoodListUI(foodData, true)

    }


    if (foodListContainer)
        updateFoodList(categoryParam)


    const updateCategoryList = async () => {
        const categoryData = await getData('api/category-list/')
        categoryListContainer.innerHTML = ``
        if (categoryData.length <= 0) {
            categoryListContainer.classList.add("justify-content-center")
            categoryListContainer.innerHTML = `
            <div class="col-12 ">
                   <div class="card bg-transparent border-0">
                        <div class="card-body d-grid text-center">
                            <i class="bi bi-search display-1"></i>
                            <p class="text-black card-text">Could not found any category</p>
                        </div>
                    </div>
            </div>
            `
        } else {
            categoryListContainer.classList.remove("justify-content-center")
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
        }


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
                    slidesPerView: 3,
                },
                1200: {
                    slidesPerView: 4
                }
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
                <span class="text-secondary">x${Number(data.quantity)}</span>
            </div>
            <div class="col-1 align-self-center">
                <button class="btn text-dark float-end shopping-cart-item-remove" data-id="${data.id}" onclick="removeItemFromShoppingCart(event)">
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

    const addBtnShoppingCartRemove = () => {
        const btnList = document.querySelectorAll(".shopping-cart-item-remove")
        btnList.forEach(button => {
            button.addEventListener("click", () => {

            })
        })
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
                    myCart.decreaseQuantity(loadedFood.id, 1, id, loadedFood.name)
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
                            <button type="button" class="btn btn-lg  btn-dark w-75" onclick="openShoppingCartInModal()"><i class="bi bi-cart mx-2"></i> Finish order</button>   
                            <button type="button" class="btn btn-lg  btn-outline-dark w-25" data-bs-dismiss="modal" aria-label="Close">Add more</button> 
                        </div>                        
                          
                        </div>
                    </div>
                </div>
            `
                handleSeatClick()

            })
        })
    }

    window.loadShoppingCartEvent = () => {

        shoppingCartCanvas.show()
        const ulElement = document.createElement("ul")
        ulElement.classList.add("list-unstyled", "overflow-y-auto", "overflow-x-hidden")
        myCart.items.forEach(item => {
            const fullData = FOOD_LIST.filter(food_item => food_item.id == item.id)[0]
            if (fullData) {
                fullData["quantity"] = item.quantity
                ulElement.innerHTML += checkoutTemplate.apply(fullData)
            }
        })
        shoppingCartBody.innerHTML = ''
        shoppingCartBody.appendChild(ulElement)

    }

    window.openShoppingCartInModal = () => {
        orderModal.hide()
        loadShoppingCartEvent()
    }
    window.removeItemFromShoppingCart = (e) => {
        const id = e.currentTarget.getAttribute("data-id")
        myCart.removeItem(id)
        loadShoppingCartEvent()

    }

    window.onWindowResize = (mediaQuery, callback) => {
        const mediaQueryList = window.matchMedia(mediaQuery);

        const handleWindowSizeChange = (mediaQueryList) => {
            if (mediaQueryList.matches) {
                callback();
            }
        };
        handleWindowSizeChange(mediaQueryList);

        const resizeHandler = () => handleWindowSizeChange(mediaQueryList);
        window.addEventListener('resize', resizeHandler);

        return {
            removeListener: () => {
                window.removeEventListener('resize', resizeHandler);
            },
        };
    }

    if (shoppingCartBtn)
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


