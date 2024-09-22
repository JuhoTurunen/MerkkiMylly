
document.getElementById('click-button').addEventListener('click', function(event) {
    event.preventDefault();
    const clickUrl = event.target.getAttribute("click-url");
    
    fetch(clickUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error:", data.error);
        } else {
            console.log("Clicks:", data.clicks);
            console.log("Click Buffer:", data.click_buffer);
            console.log("Points:", data.points);
            console.log("Point Buffer:", data.point_buffer);
            document.getElementById('clicks').innerHTML = data.clicks + data.click_buffer;
            document.getElementById('points').innerHTML = data.points + data.point_buffer;
        }
    })
    .catch(error => console.error("Request failed:", error));
});