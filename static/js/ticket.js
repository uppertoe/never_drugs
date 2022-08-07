const form = document.getElementById("form")

form.addEventListener('submit' ,(e)=>{
  e.preventDefault();
  console.log('hi');
  const formData = new FormData(form);

  fetch(ticket_url,{
    method: 'post',
    headers: {"X-Requested-With": "XMLHttpRequest"},
    body:formData
  })
  .then((response)=>response.json())
  .then((text)=>console.log(text))
  .catch((error)=>console.error(error))
})