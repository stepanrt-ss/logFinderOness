document.getElementById('start-search').addEventListener('click', function () {

    const date = document.getElementById('dateRange').value
    let first_date = null
    let second_date = null
    let nicknames = document.getElementById('input-nickname').value
    const check_global = document.getElementById('use-global-chat').checked
    const check_local = document.getElementById('use-local-chat').checked
    const check_commands = document.getElementById('use-commands-chat').checked
    const check_discipline_commands = document.getElementById('use-discipline-commands-chat').checked
    const check_pm = document.getElementById('use-pm-chat').checked
    const server_id = document.getElementById('select-server').value

    if (date === '') {
        alert('Вы не выбрали дату(')
    } else {
        if (date.length === 10) {
            first_date = date
            second_date = date
        } else {
            first_date = date.split('/')[0].replace(' ', '')
            second_date = date.split('/')[1].replace(' ', '')
        }

        if (nicknames === "") {
            nicknames = null;
        }

        let list_phrases = [];

        const checks = [
            { flag: check_global, phrases: ['[G]'] },
            { flag: check_local, phrases: ['[L]'] },
            { flag: check_commands, phrases: ['/'] },
            { flag: check_discipline_commands, phrases: ['/warn ', '/tempmute ', '/mute ', '/kick ', '/tempban ', '/ban '] },
            { flag: check_pm, phrases: ['/pm ', '/m ', '/r ', '/msg ', '/w ', '/tell '] },
        ];

        checks.forEach(check => {
            if (check.flag) {
                list_phrases.push(...check.phrases);
            }
        });

        const dataSend = JSON.stringify({
            "first_date": first_date,
            "second_date": second_date,
            "nicknames": nicknames,
            "data_search": list_phrases,
            "server_id": server_id
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
    }



})