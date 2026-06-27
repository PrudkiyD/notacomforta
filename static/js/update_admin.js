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
})