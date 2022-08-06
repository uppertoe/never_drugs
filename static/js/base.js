const navItems = document.querySelectorAll('.nav-link')

// function for use in eventListener passing in event => e
function setActive(e){
  // get the parent of the event the UL
  const parent = e.target.parentNode
  // query the parent and get the active class
  const active = parent.querySelector('.active')
  // check for active class
  if(active){
    // toggle active class
    active.classList.toggle('active')
  }
  // add active class
  e.target.classList.add('active')
}

// forEach loop defining each node as the variable listItem
navItems.forEach(listItem => {
  // running click eventListener on each listItem with our setActive function
  listItem.addEventListener("click", setActive)
})