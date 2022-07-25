var user_id = document.getElementById("user_id").textContent;
user_id = JSON.parse(user_id);

// Generate CSRFToken; From django docs: https://docs.djangoproject.com/en/4.0/ref/csrf/
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const cartBtns = document.querySelectorAll("#chg-cart");
const quantityDisplay = document.querySelectorAll('.item_qty')
const itemCard = document.querySelectorAll('.item')
const CART_URL = window.location.pathname == "/cart/" ? "update-cart/" : '/cart/update-cart/';

cartBtns.forEach((btn, idx) => {
  btn.addEventListener("click", () => {
    if (!user_id) {
      alert("You must be logged in to add to cart"); // may change
    } else {
      // user is logged in
      // send the req-type and item id, return qty and status code
      let reqType = btn.dataset.reqType;
      let itemId = btn.dataset.itemId;
      let loop = btn.dataset.loop;
      const csrftoken = getCookie("csrftoken");

      fetch(CART_URL, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ reqType, itemId }),
      })
        .then((response) => response.json())
        .then(data => {
          alert("Cart updated")
          quantityDisplay[loop-1].textContent = data['quantity'] // Go back once, index is -1 loop no.
        })
        .catch((err) => console.error(err));
    }
  });
});
