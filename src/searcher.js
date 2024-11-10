document.getElementById('start-search').addEventListener('click', function () {

    const first_date = document.getElementById('first-date').value
    const second_date = document.getElementById('second-date').value
    // const plus_keys = document.getElementById('input-plus-keys').value
    let nicknames = document.getElementById('input-nickname').value
    const check_global = document.getElementById('use-global-chat').checked
    const check_local = document.getElementById('use-local-chat').checked
    const check_commands = document.getElementById('use-commands-chat').checked
    const check_discipline_commands = document.getElementById('use-discipline-commands-chat').checked
    const check_pm = document.getElementById('use-pm-chat').checked

    if (nicknames === "") {
        nicknames = null
    }

    let list_phrases = []

    if (check_global) {
        list_phrases.push('[G]')
    }

    if (check_local) {
        list_phrases.push('[L]')
    }

    if (check_commands) {
        list_phrases.push('/')
    }

    if (check_discipline_commands) {
        list_phrases.push('/warn ', '/tempmute ', '/mute ', '/kick ', '/tempban ', '/ban ')
    }

    if (check_pm) {
        list_phrases.push('/pm ', '/m ', '/r ', '/msg ', '/w ', '/tell ')
    }

    const dataSend = JSON.stringify({
        "first_date": first_date,
        "second_date": second_date,
        "nicknames": nicknames,
        "data_search": list_phrases
    })

    fetch('public/loading.html')
        .then(response => response.text())
        .then(html => document.getElementById('loading').innerHTML = html)

    fetch('http://localhost:5000/getLogs', {
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