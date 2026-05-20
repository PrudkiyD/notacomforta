console.log('static')

try{
    if(document.querySelector('.des-text')){
        const des_text = document.querySelector('.des-text')
        let link = des_text.querySelectorAll('a')
        for(let l in link){
            link[l].parentElement.className = 'activeLinkind'
        }
    }
}
catch{
    console.log('desUrlError')
}





const ul = document.querySelector('.catalog-menu').querySelectorAll('li')


try{
    document.querySelectorAll('.c-price').forEach(el=>{
        let num = el.innerText.split(' ')
        el.innerText = ''
        num.forEach(n=>{
            if (new Intl.NumberFormat('ru-RU').format(n) != 'не число'){
                el.innerText += ` ${new Intl.NumberFormat('ru-RU').format(n)}`
            }else{
                el.innerText += ` ${n}`
            }
        })
    })
    
}catch{}
