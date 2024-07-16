const allStar = document.querySelectorAll('.rating .star');
const ratingValue = document.querySelector('.rating input');

allStar.forEach((item, idx) => {
    item.addEventListener('click', function() {
        ratingValue.value = idx + 1;
        console.log(ratingValue.value);

        allStar.forEach(i => {
            i.classList.replace('bxs-star', 'bx-star');
            i.classList.remove('active');
        });

        for (let i = 0; i <= idx; i++) {
            allStar[i].classList.replace('bx-star', 'bxs-star');
            allStar[i].classList.add('active');
        }
    });
});
