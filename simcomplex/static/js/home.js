window.onload = function() {
    const blob = document.getElementById("blob");
    const blob2 = document.getElementById("blob2");
    
    function moveBlob() {
        const maxX = window.innerWidth - blob.clientWidth;
        const maxY = window.innerHeight - blob.clientHeight;
        
        var randomX = Math.random() * maxX;
        var randomY = Math.random() * maxY;
        
        blob.style.left = `${randomX}px`;
        blob.style.top = `${randomY}px`;
    }

    function moveBlob2() {
        const maxX = window.innerWidth - blob2.clientWidth;
        const maxY = window.innerHeight - blob2.clientHeight;
        
        var randomX = Math.random() * maxX;
        var randomY = Math.random() * maxY;
        
        blob2.style.left = `${randomX}px`;
        blob2.style.top = `${randomY}px`;
    }
    setInterval(moveBlob, 6000); // Move the blob every 6 seconds
    setInterval(moveBlob2, 6000); // Move the blob every 6 seconds
}
