document.getElementById('start-search').addEventListener('click', function () {

    const first_date = document.getElementById('first-date').value
    // const second_date = document.getElementById('second-date').value
    // const plus_keys = document.getElementById('input-plus-keys').value
    const nicknames = document.getElementById('input-nickname').value
    const check_global = document.getElementById('use-global-chat').checked
    const check_local = document.getElementById('use-local-chat').checked
    const check_commands = document.getElementById('use-commands-chat').checked
    const check_pm = document.getElementById('use-pm-chat').checked

    console.log(first_date)

    const dataSend = JSON.stringify({
        "first_date": first_date,
        // "second_data": second_date,
        // "plus_keys": plus_keys,
        "nicknames": nicknames,
        "check_global": check_global,
        "check_local": check_local,
        "check_commands": check_commands,
        "check_pm": check_pm
    })

    fetch('public/loading.html')
        .then(response => response.text())
        .then(html => document.getElementById('loading').innerHTML = html)

    fetch('http://194.87.43.6:8041/getLogs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: dataSend
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        document.getElementById('logs-area').value = data['logs']
        document.getElementById('logs-area').scrollTop = 0
    }).then(() => document.getElementById('loading-c').remove())

})