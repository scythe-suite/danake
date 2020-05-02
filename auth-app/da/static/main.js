const shotButton = document.getElementById('shot');
const submitButton = document.getElementById('submit');
const video = document.getElementById('video');
const img = document.getElementById('screenshot');
let imgBlob = null;
const canvas = document.createElement('canvas');

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

shotButton.onclick = video.onclick = function () {
  console.log(video.strObject);
  if (!video.srcObject) {
    console.log('getting stream');
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = shot;
      })
      .catch(error => console.error('mediaDevices error:', error));
  } else shot();
};

submitButton.onclick = function () {
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
    console.log('got:', json);
    document.cookie = json['cookie'];
    document.location = '/cs/';
  })
  .catch(error => console.log('fetch error:', error));
}