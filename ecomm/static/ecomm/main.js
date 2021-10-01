function updateCartBadge() {
  url = "/api/getcartquantity";
  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
  }).then((response) => {
    const element = document.getElementById("cart-quantity-badge");
    if (response) {
      response.json().then((data) => {
        if (parseInt(data.data) > 99) {
          element.innerHTML = "99" + "+";
        } else {
          element.innerHTML = data.data;
        }
      });
      
    }
  });
}

const element = document.getElementById("review-stars");
if (element) {
  const reviewCount = element.innerHTML;
  if (reviewCount) {
    element.innerHTML = '<i class="bi bi-star-fill"></i>';
    let c = Math.floor(parseFloat(reviewCount));
    for (let i = 1; i < c; i++) {
      element.insertAdjacentHTML(
        "beforeend",
        '<i class="bi bi-star-fill"></i>'
      );
    }
    if (parseFloat(reviewCount) - c >= 0.5) {
      element.insertAdjacentHTML(
        "beforeend",
        '<i class="bi bi-star-half"></i>'
      );
    }
  }
}

window.onload = updateCartBadge;