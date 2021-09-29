function updateCartBadge() {
<<<<<<< HEAD
	var elements = document.getElementsByClassName('cart-quantity-badge')
=======
	
>>>>>>> dev
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
		for (var element of elements) {
			if (parseInt(data.data) > 99){
				element.innerHTML = '99+'
			} else{
				element.innerHTML = data.data
			}
		}
	})
}

window.onload = updateCartBadge



					