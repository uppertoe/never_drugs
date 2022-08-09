const form = document.getElementById("form-ticket");
const button = document.getElementById("btn-ticket-submit")
const fieldset = document.getElementById("fieldset-ticket")
const spinner = document.createElement("span");

function dataSent() {
    fieldset.setAttribute("disabled", "");
    spinner.classList.add("spinner-border", "spinner-border-sm", "mx-2");
    button.innerText = "Sending...";
    button.prepend(spinner);
}

function responseReceived() {
    spinner.remove();
    button.classList.remove("btn-primary");
    button.classList.add("btn-success");
    button.innerText = "Sent";
}

function responseError() {
    spinner.remove();
    button.classList.remove("btn-primary");
    button.classList.add("btn-danger");
    button.innerText = "Failed to send";
}

form.addEventListener('submit' ,(e)=>{
  e.preventDefault();
  const formData = new FormData(form);
  dataSent();

  fetch(ticket_url,{
    method: 'post',
    headers: {"X-Requested-With": "XMLHttpRequest"},
    body:formData
  })
  .then((response)=> response.json())
  .then((data)=> {
    console.log(data);
    responseReceived();
    })
  .catch((error)=> {
    console.error(error);
    responseError();
  })
})