const sendButtons = document.getElementById('send');
const testButton = document.getElementById('test');
const formElement = document.getElementById('form');
const modalElement = document.getElementById('modal');
const responseTitleElement = document.getElementById('response-title');
const responseBodyElement = document.getElementById('response-body');

window.onclick = function(e){
  if (e.target == modal) modal.style.display = "none";
}

document.onkeydown = function(evt) {
  evt = evt || window.event;
  let isEscape = false;
  if ("key" in evt) isEscape = (evt.key === "Escape" || evt.key === "Esc");
  else isEscape = (evt.keyCode === 27);
  if (isEscape) modal.style.display = "none";
};

function submit(evt, mode) {
  let formData =  new FormData(formElement);
  formData.append('mode', mode);
  fetch('', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(json => {
    console.log('got:', json);
    responseTitleElement.innerHTML = json.title;
    responseBodyElement.innerHTML = json.body;
    modalElement.style.display = 'block';
  })
  .catch(error => console.log('fetch error:', error));
  evt.preventDefault();
}

sendButtons.onclick = evt => submit(evt, 'send')
testButton.onclick = evt => submit(evt, 'test')