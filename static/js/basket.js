document.addEventListener("DOMContentLoaded", function () {
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
                <div class="cart-item">
                    <div>
                        <img width="150" src="${item.img}">
                    </div>
                    <div>
                        <h3>${item.product_name}</h3>
                        <p>Кількість: ${item.quantity}</p>
                        <p>Ціна: ${item.price_per_unit} грн</p>
                    </div>
                </div>
                
            `;
        });

        itemsHTML += `<hr><div class="cart-summary">Загальна сума: ${totalSum} грн</div>`;

        // Вставляємо HTML у контейнер
        cartContainer.innerHTML = itemsHTML;

    }

    // Основна функція для перевірки ключа
    async function checkAndFetchCart() {
        const cartKey = localStorage.getItem(localStorageKey);

        if (cartKey) {
            console.log("Cart key found:", cartKey);
            // Якщо ключ є, надсилаємо запит на /order/cart/[cart_key]
            const url = `/order/cart/${cartKey}`;
            const cartData = await fetchCart(url);
            console.log("Cart data:", cartData);

            // Відображаємо товари у кошику
            renderCart(cartData);
        } else {
            console.log("Cart key not found, creating a new one...");
            // Якщо ключа немає, надсилаємо запит на /order/cart/create-key
            const url = `/order/cart/create-key`;
            const cartData = await fetchCart(url);

            if (cartData && cartData.cart_key) {
                // Зберігаємо новий ключ у localStorage
                localStorage.setItem(localStorageKey, cartData.cart_key);
                console.log("New cart key saved:", cartData.cart_key);

                // Після створення ключа повторно отримуємо кошик
                const newCartUrl = `/order/cart/${cartData.cart_key}`;
                const newCartData = await fetchCart(newCartUrl);
                renderCart(newCartData);
            } else {
                console.error("Failed to create cart key");
                cartContainer.innerHTML = "<p>Помилка отримання кошика</p>";
            }
        }
    }

    // Виконуємо перевірку та отримання кошика
    checkAndFetchCart();
});

document.querySelector('.checkout').addEventListener('click', function(){
    localStorage.removeItem("cart_key");
})