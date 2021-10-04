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

// helpful review function
const helpfulReviewButtons = document.getElementsByClassName(
  "helpful-review-button"
);

for (const element of helpfulReviewButtons) {
  element.addEventListener("click", function () {
    var reviewID = this.dataset.reviewid;
    // console.log('productId', productId, 'action', action)
    if (user === "AnonymousUser") {
      console.log(AnonymousUser);
    } else {
      helpfulReview(reviewID);
    }
  });
}

function helpfulReview(reviewID) {
  var url = "/api/review/helpful";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ "reviewID": reviewID })
  }).then((response) => {
    return response.json()
  }).then( data => {
    location.reload()
  }).catch(e => console.log(e))
}

// enables bootstrap popover
// [...document.querySelectorAll('[data-bs-toggle="popover"]')]
//   .forEach(el => new bootstrap.Popover(el))
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl, {
    html: true,
  })
})

var popover = new bootstrap.Popover(document.querySelector('.review-popover'), {
  container: 'body',
  html: true
})