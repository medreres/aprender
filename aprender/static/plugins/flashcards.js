function flip(flipCard) {
    flipCard.classList.toggle('flipped');
}

function slideNext() {
    const myCarouselEl = document.querySelector('#carouselExampleInterval')
    const carousel = bootstrap.Carousel.getInstance(myCarouselEl) // Retrieve a Carousel instance
    carousel.next();
}

function slidePrev() {
    const myCarouselEl = document.querySelector('#carouselExampleInterval')
    const carousel = bootstrap.Carousel.getInstance(myCarouselEl) // Retrieve a Carousel instance
    carousel.prev();
}

document.addEventListener('DOMContentLoaded', () => {
    currentWord();
})

function currentWord() {
    fetch(`${path}/sets/${idOfSet}/currentWord`)
        .then(response => response.json())
        .then(result => {
            // go to the next flipcard and change it contexr
            let frontSide = document.querySelector('#carouselItemOneFront');
            frontSide.innerHTML = result['word'];

            let flipSide = document.querySelector('#carouselItemOneBack');
            flipSide.innerHTML = result['definition'];

            let progressBar = document.querySelector('#progressFlashCards');
            progressBar.innerHTML = `${result['index']}/${result['allWordsCount']}`;
            setProgressBar(result);
        })
}

function nextWord() {

    fetch(`${path}/sets/${idOfSet}/nextWord`)
        .then(response => response.json())
        .then(result => {
            let nextSlide = document.querySelector('.carousel-item:not(.active)');
            let front = nextSlide.querySelector('.flip-card-front');
            let back = nextSlide.querySelector('.flip-card-back');
            front.innerHTML = result['word'];
            back.innerHTML = result['definition'];

            let progressBar = document.querySelector('#progressFlashCards');
            progressBar.innerHTML = `${result['index']}/${result['allWordsCount']}`;
            setProgressBar(result);
            slideNext();
            resetFlip();
        })
}

function resetFlip() {
    document.querySelectorAll('.flipped').forEach(card => {
        if (card.classList.contains('flipped'))
            card.classList.remove('flipped');
    })
}

function prevWord() {
    fetch(`${path}/sets/${idOfSet}/prevWord`)
        .then(response => response.json())
        .then(result => {
            let nextSlide = document.querySelector('.carousel-item:not(.active)');
            let front = nextSlide.querySelector('.flip-card-front');
            let back = nextSlide.querySelector('.flip-card-back');
            front.innerHTML = result['word'];
            back.innerHTML = result['definition'];

            let progressBar = document.querySelector('#progressFlashCards');
            progressBar.innerHTML = `${result['index']}/${result['allWordsCount']}`;
            setProgressBar(result);
            slidePrev();
            resetFlip();
        })
}

function setProgressBar(result) {
    let progressBar = document.querySelector('#progressBar');
    progressBar.style.width = `${result['index'] * 100 / result['allWordsCount']}%`;
}