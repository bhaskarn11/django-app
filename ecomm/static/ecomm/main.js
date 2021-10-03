// function updateCartBadge() {
const cartCountBadges = document.getElementsByClassName("cart-quantity-badge");
url = "/api/getcartquantity";
fetch(url, {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": csrftoken,
  },
}).then((response) => {
  if (response) {
    response.json().then((data) => {
      for (const element of cartCountBadges) {
        if (parseInt(data.data) > 99) {
          element.innerHTML = "99" + "+";
        } else {
          element.innerHTML = data.data;
        }
      }
    });
  }
});
// }

// window.onload = updateCartBadge

const elements = document.getElementsByClassName("review-stars");
if (elements) {
  function reviewStarGenerator(element) {
    const reviewCount = element.innerHTML;
    if (parseFloat(reviewCount)) {
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

  for (const element of elements) {
    reviewStarGenerator(element);
  }
}
