function updateCartBadge() {

	url = '/api/getcartquantity'
	fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
	}).then(response => {
		return response.json();
	}).then(data => {
		var elements = document.getElementsByClassName('cart-quantity-badge')
		for (var element in elements) {
			if (parseInt(data.data) > 99){
				element.innerHTML = '99+'
			} else{
				element.innerHTML = data.data
			}
		}
	})
}

window.onload = updateCartBadge



					