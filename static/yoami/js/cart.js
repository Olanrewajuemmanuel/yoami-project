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
const removeCartBtns = document.querySelectorAll(".remove");
const quantityDisplay = document.querySelectorAll(".item_qty");
const orderPrice = document.querySelectorAll(".order-price");
const total = document.querySelectorAll(".total");
const itemCard = document.querySelectorAll(".item");
const CART_URL =
  window.location.pathname == "/cart/" ? "update-cart/" : "/cart/update-cart/";

cartBtns.forEach((btn, idx) => {
  btn.addEventListener("click", () => {
    if (!user_id) {
      triggerModal("You must be logged in to add to cart"); // may change
    } else {
      // user is logged in
      // send the req-type and item id, return qty and status code
      
      updateCart(btn)
        
    }
  });
});

function updateCart(btn) {
      const csrftoken = getCookie("csrftoken");
      let reqType = btn.dataset.reqType
      let itemId = btn.dataset.itemId
      let loop = btn.dataset.loop
      fetch(CART_URL, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ reqType, itemId }),
      })
        .then((response) => response.json())
        .then((data) => {
          triggerModal("Cart Updated, quantity in cart: " + data["quantity"]);

          if (data["quantity"] == 0) {
            btn.disabled = true; // no value below 0 is allowed
          } else {
            removeCartBtns[loop-1].disabled = false // make specific remove button active again
          }

          quantityDisplay[loop - 1].textContent = data["quantity"]; // Go back once, index is -1 loop no.
          calcTotal(data['quantity'], orderPrice[loop-1].dataset.price, loop)
          

        })
        .catch((err) => console.error(err));
        }

function triggerModal(msg) {
  $(".message").html(msg);
  $("#YoamiModal").modal("show");
}

function calcTotal(qty, price, loopNo) {
  let orderTotal = Number.parseFloat(price) * Number.parseInt(qty)
  orderTotal = orderTotal.toFixed(2)
  total[loopNo-1].textContent =  `$${orderTotal}`
}
