const pointsElement = document.getElementById('points');
const passivePower = pointsElement.getAttribute('passive-power') / 100;
let currentPoints = Number(pointsElement.innerHTML);
let lastUpdate = performance.now();

function updatePoints(timestamp) {
    const deltaTime = timestamp - lastUpdate;
    if (deltaTime >= 10) {
        const pointsToAdd = (deltaTime / 10) * passivePower;
        currentPoints += pointsToAdd;
        pointsElement.innerHTML = Math.floor(currentPoints);
        lastUpdate = timestamp;
    }
    requestAnimationFrame(updatePoints);
}

requestAnimationFrame(updatePoints);


document.getElementById('click-button').addEventListener('click', function(event) {
    event.preventDefault();
    const clickUrl = event.target.getAttribute("click-url");
    const csrf = event.target.getAttribute("csrf_token");
    
    fetch(clickUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "csrf": csrf
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
            currentPoints = data.points + data.point_buffer
        }
    })
    .catch(error => console.error("Request failed:", error));
});
