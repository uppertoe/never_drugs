const display_pane = document.getElementById("display-pane");
const review_link = document.querySelectorAll('.review_link');

function createSpinner() {
    const spinner = document.createElement("span");
    spinner.classList.add("spinner-border", "p-3", "mx-auto", "my-5", "d-flex");
    display_pane.innerHTML = spinner.outerHTML;
}

function createMessage(text) {
    const message = document.createElement("p");
    message.classList.add("m-auto");
    message.innerText = text;
    display_pane.innerHTML = message.outerHTML;
}

function toggleActive(nodelist) {
    nodelist.forEach((item) => item.classList.remove("active"))
}

review_link.forEach(item => {
    item.addEventListener('click', e => {
        e.preventDefault();
        toggleActive(review_link)
        item.classList.toggle("active");
        url = item.getAttribute("ajax");
        createSpinner();
        fetch(url, {
            method: 'get',
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.html) {
                    const html = data.html;
                    display_pane.innerHTML = html;
                } else {
                    const status = data.status;
                    display_pane.innerText = status;
                }
            })
            .catch((error) => {
                console.error(error);
                createMessage("Connection lost");
            })
    })
})
