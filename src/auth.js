document.getElementById('auth-btn').addEventListener('click', function () {

    // fetch('/src/auth.php', {
    //     method: 'POST',
    //     headers: {"Content-Type": "application/json"}
    // })

    const login = document.getElementById('login').value
    const password = document.getElementById('password').value

    fetch('/src/auth.php', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'login': login, 'password': password})
    }).then(function (response) {
        return response.json()
    })
})
