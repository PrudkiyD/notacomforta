window.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(function(){
        const elements = document.querySelectorAll('h3');
        elements.forEach(element => {
            let parent = element.parentElement
            element.innerHTML += `<p>Ціна: ${parent.querySelector('.change_prices').textContent } грн.</p>`
            parent.querySelector('fieldset').style = 'display:none;'
        });
    },1000)
    
});

window.addEventListener('click', function(element) {
    if (element.target.tagName === 'H3') {
        const fieldset = element.target.parentElement.querySelector('fieldset');
        
        console.log(fieldset.style.display)

        if (fieldset.style.display === 'block') {
            fieldset.style.display = 'none'; // Сховати
        } else {
            fieldset.style.display = 'block'; // Показати
        }
    }
});