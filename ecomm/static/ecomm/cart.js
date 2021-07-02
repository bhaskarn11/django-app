var updateButtons = document.getElementsByClassName('update-cart')

for (const updateButton of updateButtons) {
	updateButton.addEventListener('click', function () {
		var productId = this.dataset.product
		var action = this.dataset.action
		// console.log('productId', productId, 'action', action)
		if (user === 'AnonymousUser'){
			console.log(AnonymousUser)
		} else {
			updateCart(productId, action)
		}
	})
}


function updateCart(productId, action) {
	// body...
	var url = '/updatecart'

	fetch(url,{
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({'productId': productId, 'action': action})
	}).then(response => {
		return response.json();
	}).then(data => {
		location.reload()
	})
}