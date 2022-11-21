const review_textarea = document.getElementById('reviewTextarea');
const btn_save = document.getElementById('btnSave');
const btn_revert = document.getElementById('btnRevert');
const revert_text = document.getElementById('revertComment');
const auto_update_delay_ms = 500
var text_changed = false;
// implemented in template:
// const review_id
// const session_id
// const update_url
// const save_url
// const revert_url

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function getData() {
    data = {
        'review_id': review_id,
        'session_id': session_id,
        'latest_comment': review_textarea.value,
    }
    return JSON.stringify(data);
}

function saveChanges() {
    fetch(save_url, {
        method: 'post',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: getData(),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            revert_text.innerHTML = data.latest_comment_html;
            review_textarea.value = data.latest_comment;
        })
        .catch((error) => {
            console.error(error);
        })
}

function revertChanges() {
    fetch(revert_url, {
        method: 'post',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: getData(),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            revert_text.innerHTML = data.latest_comment_html;
            review_textarea.value = data.latest_comment;
            modalRevert = document.getElementById('confirmRevert');
            modal = bootstrap.Modal.getInstance(modalRevert);
            modal.hide()
        })
        .catch((error) => {
            console.error(error);
        })
}

function autoUpdate() {
    fetch(update_url, {
        method: 'post',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: getData(),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.error(error);
        })
}

function updateTimer() {
    if (text_changed === true) {
        autoUpdate()
        text_changed = false
    }
}

btn_save.addEventListener('click', (e) => {
    e.preventDefault();
    saveChanges();
})

btn_revert.addEventListener('click', (e) => {
    e.preventDefault();
    revertChanges();
})

review_textarea.addEventListener('input', (e) => {
    text_changed = true
})

setInterval(updateTimer, auto_update_delay_ms);
