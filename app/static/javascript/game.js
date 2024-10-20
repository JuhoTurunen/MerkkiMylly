const pointsElement = document.getElementById("points");
let passivePower = pointsElement.getAttribute("passive-power") / 100;
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

function flash(message, type) {
  let flashes = document.getElementById("flashes");
  flashes.textContent = "";
  let flash = document.createElement("div");
  flash.innerHTML = message;
  flash.classList.add("alert", type);
  flashes.appendChild(flash);
}

document.getElementById("click-button").addEventListener("click", function (event) {
  event.preventDefault();
  const clickUrl = event.target.getAttribute("click-url");
  const csrf = event.target.getAttribute("csrf-token");

  fetch(clickUrl, {
    method: "POST",
    headers: { csrf: csrf },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        flash(data.error, "error");
      } else {
        console.log("Clicks:", data.clicks);
        console.log("Click Buffer:", data.click_buffer);
        console.log("Points:", data.points);
        console.log("Point Buffer:", data.point_buffer);
        document.getElementById("clicks").innerHTML = data.clicks + data.click_buffer;
        currentPoints = data.points + data.point_buffer;
      }
    })
    .catch((error) => console.error("Request failed: ", error));
});

document.addEventListener("DOMContentLoaded", function () {
  const upgradeRows = document.getElementById("upgrade-rows");
  const csrf = upgradeRows.getAttribute("csrf-token");
  const buyUrl = upgradeRows.getAttribute("buy-url");

  Array.prototype.forEach.call(upgradeRows.children, function (row) {
    let form = row.getElementsByTagName("form")[0];
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      fetch(buyUrl, {
        method: "POST",
        headers: { csrf: csrf },
        body: new FormData(form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            flash(data.error, "error");
          } else {
            let priceSpan = document.getElementById("price-span-" + data.upgrade_id);
            let amountSpan = document.getElementById("amount-span-" + data.upgrade_id);
            priceSpan.innerHTML = data.price;
            amountSpan.innerHTML = data.buy_amount + Number(amountSpan.innerHTML);
            passivePower = data.passive_power / 100;
            currentPoints = data.remaining_points;
            flash("Successful purchase!", "success");
          }
        })
        .catch((error) => console.error("Request failed: ", error));
    });
  });
});
