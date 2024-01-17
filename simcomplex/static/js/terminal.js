function toggleCamera() {
    var c = document.getElementById('camera-container');
    var cc2 = document.getElementById('cc2');
    var bg = document.getElementById('camerabg');
    // Calculate the width of the navbar dynamically
    var cWidth = c.offsetWidth;

    // Toggle the right position of the navbar to show/hide it
    if (c.style.right === "0px") {
      c.style.right = `calc(-${cWidth}px)`;
      cc2.style.right = `calc(-${cWidth}px)`;
      bg.style.right = `calc(-${cWidth}px)`;
    } else {
        c.style.right = "0";
        cc2.style.right = "0";
        bg.style.right = "0";
    }
}
window.addEventListener('resize', function() {
    var c = document.getElementById('camera-container');
    var cc2 = document.getElementById('cc2');
    var bg = document.getElementById('camerabg');
    // Recalculate the width of the camera
    var cameraWidth = c.offsetWidth;

    // Update the right position of the camera
    if (c.style.right != cameraWidth*-1) {
        c.style.right = `calc(-${cameraWidth}px)`;
        cc2.style.right = `calc(-${cameraWidth}px)`;
        bg.style.right = `calc(-${cameraWidth}px)`;
    }
  });

const socket = io.connect(window.location.origin);
