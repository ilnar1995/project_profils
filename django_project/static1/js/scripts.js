// Add star rating
const rating = document.querySelector('form[name=rating]');
const likeBtnOne = rating.querySelector('#movie_like_btn');
const dislikeBtnOne = rating.querySelector('#movie_dislike_btn');
const idMovieOne = rating.querySelector('#id_movie');
const vote1One = rating.querySelector('#id_vote_1');
const vote2One = rating.querySelector('#id_vote_2');

likeBtnOne.addEventListener('click', () => {
    vote1One.checked = true;
    vote2One.checked = false;
});
dislikeBtnOne.addEventListener('click', () => {
    // Получаем данные из формы
    vote1One.checked = false;
    vote2One.checked = true;
});

rating.addEventListener("click", function (e) {
    e.preventDefault();
    // Получаем данные из формы
    if(e.target.classList.contains('rating_modiff')){
        let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
    }

});

const __comments = document.querySelectorAll(".comm-item");
const rating1 = document.querySelector('form[name=dlemasscomments]');

__comments.forEach(__comment => {
    const text = __comment.querySelector(".comment__text");
    const like = __comment.querySelector(".comment__like");
    const dislike = __comment.querySelector(".comment__dislike");

    like.addEventListener("click", (e) => {
        e.preventDefault();
        let data = new FormData(rating1);
        data.append("vote", "1");
        data.append("Review", `${text.id}`);
        fetch(rating1.action, {
            method: 'POST',
            body: data
        })
            .then(response => alert("Лайк установлен"))
            .catch(error => alert("Error"))
    });
    dislike.addEventListener("click", (e) => {
        e.preventDefault();
        let data = new FormData(rating1);
        data.append("vote", "-1");
        data.append("Review", `${text.id}`);
        fetch(rating1.action, {
            method: 'POST',
            body: data
        })
            .then(response => alert("Дизлайк установлен"))
            .catch(error => alert("Ошибка"))
    });
});

window.onload = function(){
    slideOne();
    slideTwo();
}
let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1").max;
function slideOne(){
    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = sliderOne.value;
    fillColor();
}
function slideTwo(){
    if(parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap){
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = sliderTwo.value;
    fillColor();
}
function fillColor(){
    percent1 = (sliderOne.value / sliderMaxValue) * 100;
    percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, #dadae5 ${percent1}% , #3264fe ${percent1}% , #3264fe ${percent2}%, #dadae5 ${percent2}%)`;
}
