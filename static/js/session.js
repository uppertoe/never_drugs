const display_pane = document.getElementById("display-pane");
console.log(display_pane)

document.querySelectorAll('.review_link').forEach(item => {
    item.addEventListener('click', e => {
        e.preventDefault();
        url = item.href;
    
        fetch(url, {
            method: 'get',
            headers: {"X-Requested-With": "XMLHttpRequest"}
        })
        .then((response)=> response.json())
        .then((data)=> {
            const html = decodeURIComponent(data.html)
            console.log(html);
            console.log(display_pane)
            display_pane.innerHTML = html;
        })
        .catch((error)=> {
            console.error(error);
        })
    })
})

