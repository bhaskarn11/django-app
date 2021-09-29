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
					element.innerHTML = '99' + '+'
				} else{
					element.innerHTML = data.data
				}
			})
		}
	})
}

window.onload = updateCartBadge


