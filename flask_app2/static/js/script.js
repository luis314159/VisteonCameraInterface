function startStream() {
    var cameraId = document.getElementById('cameraSelect').value;
    var videoStream = document.getElementById('videoStream');
    videoStream.src = '/video_feed?camera_id=' + cameraId;
}

function saveImage(color) {
    var cameraId = document.getElementById('cameraSelect').value;
    fetch(`/save_image?camera_id=${cameraId}&color=${color}`, {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            showMessage('Image saved successfully!');
        } else {
            showMessage('Error saving image.');
        }
    });
}

function showMessage(message) {
    var messageDiv = document.getElementById('message');
    messageDiv.innerText = message;
    messageDiv.style.display = 'block';
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 3000);  // Message disappears after 3 seconds
}
