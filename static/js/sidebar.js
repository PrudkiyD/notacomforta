const burger = document.querySelector('#burger');
const sidebar = document.querySelector('#sidebar');
const burger_icone = document.querySelector('#burger-icone');
const sidebar_bloc = document.querySelector('#sidebar-bloc');


window.addEventListener('click', function(ev){
    if(ev.target.id === 'burger-icone'){
        sidebar.classList.toggle('active')
        burger_icone.classList.toggle('burger-active')
        sidebar_bloc.classList.toggle('active-sidebar')
    }

    if(ev.target.id === 'sidebar'){
        sidebar.classList.toggle('active')
        burger_icone.classList.toggle('burger-active')
        sidebar_bloc.classList.toggle('active-sidebar') 
    }

    if(ev.target.className === 'searchFilter'){
        sidebar.classList.toggle('active')
        burger_icone.classList.toggle('burger-active')
        sidebar_bloc.classList.toggle('active-sidebar')
    }
})



/* active burger-active active-sidebar */


















