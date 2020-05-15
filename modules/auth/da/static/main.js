const responseTitleElement = document.getElementById('response-title');
const responseBodyElement = document.getElementById('response-body');
const modalElement = document.getElementById('modal');

const loaderElement = document.getElementById('loader');
const camerauiElement = document.getElementById('cameraui');

const shotButton = document.getElementById('shot');
const submitButton = document.getElementById('submit');
const video = document.getElementById('video');
const img = document.getElementById('screenshot');
const canvas = document.createElement('canvas');

let imgBlob = null;

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

function shot() {
  video.classList.add('pure-img-bordered');
  img.classList.add('pure-img-bordered');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  submitButton.style.display = 'block';
  img.src = canvas.toDataURL();
  canvas.toBlob(blob => imgBlob = blob);
}

shotButton.onclick = video.onclick = function() {
  if (!video.srcObject) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = shot;
      })
      .catch(error => {
        console.error('mediaDevices error:', error)
        modalElement.style.display = 'block';
      });
  } else shot();
};

submitButton.onclick = function() {
  video.srcObject.getTracks().forEach(track => track.stop());
  video.srcObject = null;
  let formData = new FormData();
  formData.append('photo', imgBlob);
  fetch('', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(json => {
      camerauiElement.style.display = 'none';
      loaderElement.style.display = 'block';
      document.cookie = json['cookie'];
      document.location = '/cs/';
    })
    .catch(error => {
      console.log('fetch error:', error);
      responseTitleElement.innerHTML = 'Unexpected error';
      responseBodyElement.innerHTML = 'Encountered the following error while processing the server reply:\n<pre>' + error + '</pre>';
      camerauiElement.style.display = 'none';
      modalElement.style.display = 'block';
    });
}