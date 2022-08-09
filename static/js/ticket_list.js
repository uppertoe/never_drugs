const selfRadio = document.getElementById("btnradio-self");
const allRadio = document.getElementById("btnradio-all");
const selfTicketList = document.getElementById("self-tickets");
const allTicketList = document.getElementById("all-tickets");

selfRadio.addEventListener("click", (e)=> {
    selfTicketList.style.display = "block";
    allTicketList.style.display = "none";
})

allRadio.addEventListener("click", (e)=> {
    allTicketList.style.display = "block";
    selfTicketList.style.display = "none";
})