document.addEventListener('DOMContentLoaded', function() {
    let objectTools = document.querySelector('.object-tools')
    let actions = document.querySelector('.actions')

    if(objectTools){
        objectTools.innerHTML += `<li>
                                    <a href="/update/">
                                        Оновити товар
                                    </a>
                                </li>`
    }

    if(actions){
        actions.innerHTML += `<input type="text" id="discount-value">
                                <button type="button" class="button" data-id="change-price">Змінити ціни</button>
                                `
    }

    window.addEventListener('click', function(el){
        if(el.target.dataset.id === 'change-price'){
            let csrf = this.document.querySelector('#changelist-form').querySelector('input').value
            let discount = this.document.querySelector('#discount-value').value
            let product = []
            let resultList = this.document.querySelector('#result_list').querySelector('tbody').querySelectorAll('tr')

            resultList.forEach(element => {
                let checkBox = element.querySelector('input[name="_selected_action"]')
                if(checkBox.checked){
                    product.push(checkBox.value) 
                }
            });

            if (!['+', '-'].includes(discount[0])) {
                alert("Укажіть '+' або '-' перед значенням");
                return;
            }


            if (product.length === 0) {
                alert("Виберіть хоча б один товар!");
                return;
            }

            
            
            fetch('/update/discount/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf
                },
                body: JSON.stringify({
                    "discount": discount, 
                    "product": product
                })
            })
            .then(response => {
                // Перетворюємо відповідь у JSON
                return response.json().then(data => {
                    console.log("Відповідь сервера:", data); // Виводимо дані в консоль

                    if (data.status === 'ok') {
                        location.reload(); 
                    } else {
                        alert("Помилка: " + (data.error || "невідома помилка"));
                    }
                });
            })
            
        }
    })
});