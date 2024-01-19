const toasts = document.getElementsByClassName('toast')
const triggerToast = (item) => {
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(item)
    toastBootstrap.show()
}

for (let toast of toasts) {
    triggerToast(toast)
}