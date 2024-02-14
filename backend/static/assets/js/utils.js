export const formatDate = (date) => {
    return Intl.DateTimeFormat("en", {
        month: "short",
        year: "numeric",
        day: "2-digit",
        hour: "numeric",
        minute: "numeric"
    }).format(new Date(date));
}
export const toast = (text, duration = 5000, type = "info") => {
    let backgroundColor;

    switch (type) {
        case "info":
            backgroundColor = "linear-gradient(to right, #3498db, #2980b9)";
            break;
        case "success":
            backgroundColor = "linear-gradient(to right, #2ecc71, #27ae60)";
            break;
        case "error":
            backgroundColor = "linear-gradient(to right, #e74c3c, #c0392b)";
            break;
        case "warning":
            backgroundColor = "linear-gradient(to right, #f39c12, #d35400)";
            break;
        default:
            backgroundColor = "linear-gradient(to right, #3498db, #2980b9)";
            break;
    }

    Toastify({
        text: text,
        duration: duration,
        newWindow: false,
        close: true,
        gravity: "bottom", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: backgroundColor,
        },
    }).showToast();
}