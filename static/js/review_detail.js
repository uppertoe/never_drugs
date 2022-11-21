const review_textarea = document.getElementById('reviewCommentTextarea');
const auto_update_delay_ms = 500;
const empty_message = 'Peer review meeting comments will appear in this space'
// Implemented in template:
// const review_id
// const update_url

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
            if (data.latest_comment_html) {
                review_textarea.innerHTML = data.latest_comment_html;
            }
            else {
                const html = document.createElement("div")
                html.classList.add("text-muted")
                html.innerText = empty_message
                review_textarea.replaceChildren(html)
            }
        })
        .catch((error) => {
            console.error(error);
        })
}

setInterval(autoUpdate, auto_update_delay_ms)