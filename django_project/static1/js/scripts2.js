const likeBtn111 = document.querySelector('#movie_like_btn');
const dislikeBtn111 = document.querySelector('#movie_dislike_btn');
const idMovie = document.querySelector('#id_movie');
const rating = document.querySelector('form[name=rating]');
// const vote1 = document.querySelector('#id_vote_1');
// const vote2 = document.querySelector('#id_vote_2');



likeBtn111.addEventListener("click", (e) => {
        e.preventDefault();
        let data = new FormData(rating);
        data.append("vote", "1");
        data.append("movie", ${idMovie.value});
        fetch(rating.action, {
            method: 'POST',
            body: data
        })
            .then(response => alert("Лайк установлен"))
            .catch(error => alert("Error"))
    });
dislikeBtn111.addEventListener("click", (e) => {
    e.preventDefault();
    let data = new FormData(rating);
    data.append("vote", "-1");
    data.append("movie", ${idMovie.value});
    fetch(rating.action, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Дизлайк установлен"))
        .catch(error => alert("Ошибка"))
});
//const vote1 = document.querySelector('#id_vote_1');
//const vote2 = document.querySelector('#id_vote_2');
//const likeBtn = document.querySelector('#movie_like_btn');
//const dislikeBtn = document.querySelector('#movie_dislike_btn');
//
//likeBtn.addEventListener('click', (e)=>{
//    e.preventDefault();
//    vote1.checked = true;
//    vote2.checked = false;
//        rating.addEventListener("click", function (e) {
//    // Получаем данные из формы
//    let data = new FormData(this);
//    fetch(`${this.action}`, {
//        method: 'POST',
//        body: data
//    })
//        .then(response => alert("Рейтинг установлен"))
//        .catch(error => alert("Ошибка"))
//});
//});
//dislikeBtn.addEventListener('click', (e)=>{
//    e.preventDefault();
//    vote1.checked = false;
//    vote2.checked = true;
//    rating.addEventListener("click", function (e) {
//    // Получаем данные из формы
//    let data = new FormData(this);
//    fetch(`${this.action}`, {
//        method: 'POST',
//        body: data
//    })
//        .then(response => alert("Рейтинг установлен"))
//        .catch(error => alert("Ошибка"))
//});
//});
//
//const rating = document.querySelector('form[name=rating]');
//
//
////// Add star rating
////
//rating.addEventListener("change", function (e) {
//    // Получаем данные из формы
//    let data = new FormData(this);
//    fetch(`${this.action}`, {
//        method: 'POST',
//        body: data
//    })
//        .then(response => alert("Рейтинг установлен"))
//        .catch(error => alert("Ошибка"))
//});
