window.addEventListener('click', function(el) {

    if (el.target.dataset.action == 'cartBtn') {
        var cartWraper = document.querySelector('.cartWraper');
        cartWraper.style = 'display: flex;';
    }

    if (el.target.dataset.action == 'closeCart') {
        var cartWraper = document.querySelector('.cartWraper');
        cartWraper.style = 'display: none;';
    }

    // Додаємо товар у кошик
    if (el.target.dataset.action == 'add') {
        let message = this.document.querySelector(".message")
        message.style.display = 'flex'

        this.setTimeout(function(){
            message.style.display = 'none'
        },1000)

        const cartKey = localStorage.getItem("cart_key");
        let product_id = el.target.dataset.product;
        let price_id = el.target.dataset.price;

        let url = `/order/cart/add/${cartKey}/${product_id}/${price_id}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            checkAndFetchCart();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Плюсуємо кількість
    if (el.target.dataset.action == 'plus') {
        const cartKey = localStorage.getItem("cart_key");
        let product_id = el.target.dataset.product;
        let price_id = el.target.dataset.price;

        let url = `/order/cart/add/${cartKey}/${product_id}/${price_id}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            checkAndFetchCart();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Мінусуєм кількість
    if (el.target.dataset.action == 'minus') {
        const cartKey = localStorage.getItem("cart_key");
        let product_id = el.target.dataset.product;
        let price_id = el.target.dataset.price;

        let url = `/order/cart/minus/${cartKey}/${product_id}/${price_id}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Після успішного додавання оновлюємо кошик
            checkAndFetchCart();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

window.addEventListener('change', function(el) {
    if (el.target.dataset.action == 'quantity') {
        const cartKey = localStorage.getItem("cart_key");
        let product_id = el.target.dataset.product;
        let price_id = el.target.dataset.price;

        let url = `/order/cart/quantity/${cartKey}/${product_id}/${price_id}/${el.target.value}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            checkAndFetchCart();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
})

const localStorageKey = "cart_key"; // Ключ для збереження у localStorage
const cartContainer = document.querySelector(".cartInnerProduct"); // Контейнер для товарів

// Функція для отримання даних з сервера
async function fetchCart(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching cart:", error);
        return null;
    }
}

// Функція для відображення товарів у DOM
function renderCart(cartData) {
    if (!cartData || !cartData.items || cartData.items.length === 0) {
        cartContainer.innerHTML = "<p>Кошик порожній</p>";
        return;
    }

    let totalSum = cartData.total_sum || 0;

    // Створюємо HTML для товарів
    let itemsHTML = "";

    cartData.items.forEach(item => {
        itemsHTML += `
            <tbody class="prodinCart">
                <tr class="cart-item">
                    <td>
                        <img width="150" src="${item.img}">
                    </td>
                    <td>
                        <a href="#">
                            <h3 class="nameCart">${item.product_name}</h3>
                        </a>
                        <div class="countWraper">
                            <button 
                                data-action="minus"
                                data-product="${item.product_id}" 
                                data-price="${item.price_id}"
                                >-</button>
                            <input 
                                class="numCount" 
                                data-action="quantity"
                                value="${item.quantity}"
                                data-product="${item.product_id}" 
                                data-price="${item.price_id}">
                            <button 
                                data-action="plus"
                                data-product="${item.product_id}" 
                                data-price="${item.price_id}"
                                >+</button>
                        </div>
                        <div class="priceCart">Ціна: ${item.price_per_unit} грн</div>
                    </td>
                </tr>
            </tbody>
        `;
    });

    document.querySelector('.num-product').innerText = cartData.items.length;
    itemsHTML += `<hr><div class="totalText">Загальна сума: ${totalSum} грн</div>`;

    // Вставляємо HTML у контейнер
    cartContainer.innerHTML = itemsHTML;

    
    
}

// Основна функція для перевірки ключа та оновлення кошика
async function checkAndFetchCart() {
    const cartKey = localStorage.getItem(localStorageKey);
    const cartInner = document.querySelector('.cartInner')

    if (cartKey) {
        // Якщо ключ є, надсилаємо запит на /order/cart/[cart_key]
        const url = `/order/cart/${cartKey}`;
        const cartData = await fetchCart(url);

        cartInner.classList.toggle('pulsing') 

        setTimeout(() => {
            renderCart(cartData);
            cartInner.classList.toggle('pulsing') 
        }, 1000);

        const keyInput = document.querySelector(".shopping-cart").querySelector('input[name="key"]');
        keyInput.value = cartKey;
        
    } else {
        // Якщо ключа немає, надсилаємо запит на /order/cart/create-key
        const url = `/order/cart/create-key`;
        const cartData = await fetchCart(url);

        if (cartData && cartData.cart_key) {
            // Зберігаємо новий ключ у localStorage
            localStorage.setItem(localStorageKey, cartData.cart_key);

            // Після створення ключа повторно отримуємо кошик
            const newCartUrl = `/order/cart/${cartData.cart_key}`;
            const newCartData = await fetchCart(newCartUrl);
            
            cartInner.classList.toggle('pulsing') 

            setTimeout(() => {
                renderCart(cartData);
                cartInner.classList.toggle('pulsing') 
            }, 1000);


        } else {
            console.error("Failed to create cart key");
            cartContainer.innerHTML = "<p>Помилка отримання кошика</p>";
        }
    }
}

// Виконуємо перевірку та отримання кошика при завантаженні сторінки
document.addEventListener("DOMContentLoaded", checkAndFetchCart);
