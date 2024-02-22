document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.getElementsByClassName('toast')
    const sidebarWrapper = document.querySelector(".sidebar-wrapper")
    const mainToggler = document.querySelector("#main-toggler")
    const sidebarAside = document.querySelector("#sidebar-aside")
    const backdrop = document.createElement("div")
    const btnFoodDeletes = document.querySelectorAll(".btn-food-delete")
    const btnCategoryDeletes = document.querySelectorAll(".btn-category-delete")
    const btnTipDeletes = document.querySelectorAll(".btn-tip-delete")
    const btnExtraDeletes = document.querySelectorAll(".btn-extra-delete")
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

    if (sidebarAside)
        sidebarAside.appendChild(backdrop)

    backdrop.addEventListener("click", () => {
        if (sidebarWrapper.classList.contains("active")) {
            sidebarToggle()
        }
    })

    btnFoodDeletes.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const modal = new bootstrap.Modal("#modal-food-delete", {})
            const body = modal._element.querySelector("#delete-food-body")
            const title = modal._element.querySelector("#delete-food-title")
            const input = modal._element.querySelector("#input-food-id")
            const name = e.currentTarget.getAttribute("data-name")
            const id = e.currentTarget.getAttribute("data-id")
            title.innerHTML = `Delete food`
            body.innerHTML = `
            <p class="card-text">Are you sure you want to delete ${name} ?</p>
            `
            input.value = id
            modal.show()
        })
    })

    btnCategoryDeletes.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const modal = new bootstrap.Modal("#modal-category-delete", {})
            const body = modal._element.querySelector("#delete-category-body")
            const title = modal._element.querySelector("#delete-category-title")
            const input = modal._element.querySelector("#input-category-id")
            const name = e.currentTarget.getAttribute("data-name")
            const id = e.currentTarget.getAttribute("data-id")
            title.innerHTML = `Delete category`
            body.innerHTML = `
            <p class="card-text">Are you sure you want to delete ${name} ?</p>
            `
            input.value = id
            modal.show()
        })
    })

    btnTipDeletes.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const modal = new bootstrap.Modal("#modal-tip-delete", {})
            const body = modal._element.querySelector("#delete-tip-body")
            const title = modal._element.querySelector("#delete-tip-title")
            const input = modal._element.querySelector("#input-tip-id")
            const name = e.currentTarget.getAttribute("data-name")
            const id = e.currentTarget.getAttribute("data-id")
            title.innerHTML = `Delete tip`
            body.innerHTML = `
            <p class="card-text">Are you sure you want to delete ${name} ?</p>
            `
            input.value = id
            modal.show()
        })
    })
    btnExtraDeletes.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const modal = new bootstrap.Modal("#modal-extra-delete", {})
            const body = modal._element.querySelector("#delete-extra-body")
            const title = modal._element.querySelector("#delete-extra-title")
            const input = modal._element.querySelector("#input-extra-id")
            const name = e.currentTarget.getAttribute("data-name")
            const id = e.currentTarget.getAttribute("data-id")
            title.innerHTML = `Delete extra`
            body.innerHTML = `
            <p class="card-text">Are you sure you want to delete ${name} ?</p>
            `
            input.value = id
            modal.show()
        })
    })

})