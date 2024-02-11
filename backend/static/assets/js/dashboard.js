

document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.getElementsByClassName('toast')
    const sidebarWrapper = document.querySelector(".sidebar-wrapper")
    const mainToggler = document.querySelector("#main-toggler")
    const sidebarAside = document.querySelector("#sidebar-aside")
    const backdrop = document.createElement("div")

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
})