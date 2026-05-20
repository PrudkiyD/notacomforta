let img_slid = document.querySelectorAll('.img-slid')
let img_lite = document.querySelector('.img-lite')

let btn_close = document.querySelector('.btn-close')
let obj_close = document.querySelector('#zoom-img')


for (let i in img_slid) {
    src = img_slid[i].src

    if (src) {
        img_lite.innerHTML = `${img_lite.innerHTML} <div><img src="${src}" class="item-zoom" alt=""></div>`
    }

};

let img_big = document.querySelector('.img-big')
let item_zoom = document.querySelectorAll('.item-zoom');

item_zoom.forEach(item => {
    item.addEventListener('click', function e() {
        img_big.innerHTML = `<img src="${item.src}" class="item-zoom" alt="">`
    })
})




btn_close.addEventListener("click", function (e) {
    obj_close.className = 'zoom-img-close'

});

img_slid.forEach(press => {
    press.addEventListener('click', function e() {
        img_big.innerHTML = `<img src="${press.src}" class="item-zoom" alt="">`
        obj_close.className = 'zoom-img-active'
    })
})






