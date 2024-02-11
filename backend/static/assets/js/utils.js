export const formatDate = (date) => {
    return Intl.DateTimeFormat("en", {
        month: "short",
        year: "numeric",
        day: "2-digit",
        hour:"numeric",
        minute:"numeric"
    }).format(new Date(date));
}