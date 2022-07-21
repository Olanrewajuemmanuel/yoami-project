var user = JSON.stringify('{{ user }}');
    console.log(user)
    var cartBtns = document.querySelectorAll('#cart-btn');
    cartBtns.forEach((btn) => {
        btn.addEventListener("click", (e) => {
            if (user === "AnonymousUser") {
                e.preventDefault() // Do not go to any URL
                return triggerModal()
            }
        })
    })

    function triggerModal() {
        alert('You must be logged in to add to cart')
    }