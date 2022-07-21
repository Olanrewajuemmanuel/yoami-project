var user_id = JSON.parse(document.getElementById("user_id").textContent);
var cartBtns = document.querySelectorAll("#cart-btn");
cartBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    if (!user_id) {
      e.preventDefault(); // Do not go to any URL
      return triggerModal();
    } else {
        updateCart(user_id)
    }
  });
});

function triggerModal() {
  alert("You must be logged in to add to cart");
}

function updateCart() {
    
}
