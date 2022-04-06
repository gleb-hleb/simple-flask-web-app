function delete_user(btn) {
    const userId = btn.getAttribute('data-id');

    fetch("/users/delete", {
        method: "delete",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: userId
        })
    }).then((response) => {
        if (response.status === 204) {
            console.log("Sucsess deletion.")
            const userRow = document.getElementById(`user-${userId}`);
            userRow.remove();
        } else {
            console.log("Faled deletion.")
            window.location.href = "/users";
        }
    })
}