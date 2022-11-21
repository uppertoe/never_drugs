const review_buttons = document.querySelectorAll('.review-button');
const reviews = document.querySelectorAll('.review');

function hideCurrentReview() {
    reviews.forEach((item) => item.classList.add("hide"))
}

function showReview(id) {
    const review_id = "review-" + id
    const review = document.getElementById(review_id)
    review.classList.toggle("hide")
}

function toggleActive(nodelist) {
    nodelist.forEach((item) => item.classList.remove("active"))
}

review_buttons.forEach(item => {
    item.addEventListener('click', e => {
        if (!item.classList.contains("active")) {
            toggleActive(review_buttons)
            item.classList.toggle("active")
            hideCurrentReview()
            showReview(item.id)
        }
    })
})