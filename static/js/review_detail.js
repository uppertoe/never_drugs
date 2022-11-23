// Elements
const review_textarea = document.getElementById('reviewCommentTextarea');
const connection = document.getElementById('connection');
const user_list = document.getElementById('userList');

// Variables
const auto_update_delay_ms = 500;
const empty_message = 'Peer review meeting comments will appear in this space';
const connected_message = 'Connected';
const disconnected_message = 'Connecting...';

// Implemented in template:
// const update_url

function connected() {
    const html = document.createElement("span");
    html.classList.add("badge", "bg-success", "p-2");
    html.innerText = connected_message;
    connection.replaceChildren(html);
}

function connectionLost() {
    const html = document.createElement("span");
    html.classList.add("badge", "bg-danger", "p-2");
    html.innerText = disconnected_message;
    connection.replaceChildren(html);
}

function autoUpdate() {
    fetch(update_url, {
        method: 'get',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if (data.user_list_html) { // implies session_id has been passed
                user_list.innerHTML = data.user_list_html;
                connected();
            }
            if (data.latest_comment_html) {
                review_textarea.innerHTML = data.latest_comment_html;
            }
            else { // placeholder if comment is empty
                const html = document.createElement("div");
                html.classList.add("text-muted");
                html.innerText = empty_message;
                review_textarea.replaceChildren(html);
            }
        })
        .catch((error) => {
            console.error(error);
            connectionLost();
        })
}

setInterval(autoUpdate, auto_update_delay_ms);