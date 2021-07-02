function updateCartBadge() {

	url = '/api/getcartquantity'
	fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
	}).then(response => {
		const element = document.getElementById("cart-quantity-badge")
		if (response){
			response.json().then(data => {
				if (parseInt(data.data) > 99){
					element.innerText = '99' + '+'
				} else{
					element.innerText = data.data
				}
			})
		}
	})
}

window.onload = updateCartBadge


