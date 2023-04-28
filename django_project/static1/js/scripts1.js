const filter__btn1 = document.querySelector(".filter-btn1");
const filter__wrap1 = document.querySelector(".filter-wrap1");

filter__btn1.addEventListener('click', ()=>{
    filter__wrap1.style.display = (filter__wrap1.style.display == 'none') ? 'block' : 'none';
});