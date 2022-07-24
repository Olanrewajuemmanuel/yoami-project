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

const cartBtns = document.querySelectorAll("#cart-btn");
const quantityDisplay = document.querySelectorAll('.qty-display')
const CART_URL = "cart/update-cart/";
cartBtns.forEach((btn, idx) => {
  btn.addEventListener("click", () => {
    if (!user_id) {
      alert("You must be logged in to add to cart"); // may change
    } else {
      // user is logged in
      // send the req-type and item id, return qty and status code
      let reqType = btn.dataset.reqType;
      let itemId = btn.dataset.itemId;
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
          // update QTY on front page
          qty = data['quantity']
          quantityDisplay[idx].textContent = qty
          console.log(data)
        })
        .catch((err) => console.error(err));
    }
  });
});
