const sendButtons = document.getElementById('send');
const testButton = document.getElementById('test');
const formElement = document.getElementById('form');
const modalElement = document.getElementById('modal');
const responseTitleElement = document.getElementById('response-title');
const responseBodyElement = document.getElementById('response-body');

window.onclick = e => {
  if (e.target == modal) modal.style.display = 'none';
};

document.onkeydown = evt => {
  evt = evt || window.event;
  let isEscape = false;
  if ('key' in evt) isEscape = (evt.key === 'Escape' || evt.key === 'Esc');
  else isEscape = (evt.keyCode === 27);
  if (isEscape) modal.style.display = 'none';
};

function submit(evt, mode) {
  let formData = new FormData(formElement);
  formData.append('mode', mode);
  fetch('', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(json => {
      responseTitleElement.innerHTML = json.title;
      responseBodyElement.innerHTML = json.body;
      modalElement.style.display = 'block';
    })
    .catch(error => {
      console.log('fetch error:', error);
      responseTitleElement.innerHTML = 'Unexpected error';
      responseBodyElement.innerHTML = 'Encountered the following error while processing the server reply:\n<pre>' + error + '</pre>';
      modalElement.style.display = 'block';
    });
  evt.preventDefault();
}

sendButtons.onclick = evt => submit(evt, 'send')
testButton.onclick = evt => submit(evt, 'test')