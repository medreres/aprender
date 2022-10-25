document.addEventListener('DOMContentLoaded', () => {
    currentWord();
})

const idOfSet = url.pathname.substring(url.pathname.lastIndexOf('/') + 1);

function flip(flipCard) {
    flipCard.classList.toggle('flipped');
}



function currentWord() {
    fetch(`${path}/sets/${idOfSet}/currentWord`)
        .then(response => response.json())
        .then(result => {
            // go to the next flipcard and change it contexr
            let frontSide = document.querySelector('#carouselItemOneFront');
            frontSide.innerHTML = result['word'];

            let flipSide = document.querySelector('#carouselItemOneBack');
            flipSide.innerHTML = result['definition'];

        })
}

function resetFlip() {
    document.querySelectorAll('.flipped').forEach(card => {
        if (card.classList.contains('flipped'))
            card.classList.remove('flipped');
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
            slideNext();
            resetFlip();
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
            slidePrev();
            resetFlip();
        })
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
    let questionTypes = document.querySelectorAll('input[name=questionTypes]');
    // console.log(questionTypes)
    questionTypes.forEach(checkbox => {
        checkbox.addEventListener('change', (evt) => {
            let target = evt.target;
            if (target.checked) {
                questionTypes.forEach(input => input.required = false);
            } else {
                questionTypes.forEach(input => input.required = true);
            }
        })
    })
})



function toggleLike(element) {
    const url = new URL(location.href)

    const path = `${url.origin}/sets/${setId}/toggleFavorite`;
    fetch(path)
        .then(response => response.json())
        .then(result => {
            let img = element.querySelector('img');
            if ('delete' in result) {
                // TODO replace static
                const path = heartIconPath;
                img.src = path;
                // change to blank heart
            } else {
                const path = heartRedIconPath;
                img.src = path;
            }
        })
}

function addSetToFolder(folderId) {
    console.log('click')
    const path = location.href + '/addSetToFolder';
    fetch(path, {
            method: 'POST',
            body: JSON.stringify({
                folderId: folderId
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
        })

}



var numberOfPages;


document.addEventListener('DOMContentLoaded', () => {
    // get general number of pages
    // set pagination
    getNumberOfPages();
    // load first page of words initially
    //getWords();
})


function getNumberOfPages() {
    const url = location.href + '/getNumberOfPages';
    fetch(url)
        .then(response => response.json())
        .then(result => {
            numberOfPages = result['numberOfPages'];

            // intialize pagination nav
            // upper
            $('#paginationUpper').twbsPagination({
                totalPages: numberOfPages,
                visiblePages: 3,
                onPageClick: function (evt, page) {
                    //console.log(page);
                    //$('#content').text('Page ' + page);
                    loadPage(page);
                }
            });
            // and lower
        })
}

function changeWord(element) {
    //console.log(element)
    // hide label and show input or vice versa
    toggleInput(element.dataset.id);
    if (element.dataset['changemode'] == 'false') {
        element.dataset['changemode'] = 'true';
    } else {
        element.dataset['changemode'] = 'false';
        saveWord(element.dataset.id);
    }
}

function saveWord(id) {
    let term = document.querySelector(`#term_input_${id}`).value;
    let definition = document.querySelector(`#definition_input_${id}`).value;

    // console.log(term, definition);

    document.querySelector(`#term_label_${id}`).innerHTML = term;
    document.querySelector(`#definition_label_${id}`).innerHTML = definition;

    //make post query to change the word in database
    const url = location.href + '/changeWord';
    fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                id: id,
                term: term,
                definition: definition
            })
        })
        .then(response => response.json())
        .then(result => {
            // console.log(result);
        })
}

function toggleInput(id) {
    //console.log(`term_label_${id}`);
    // for term
    document.querySelector(`#term_input_${id}`).classList.toggle('hidden');
    document.querySelector(`#term_label_${id}`).classList.toggle('hidden');

    // for definition
    document.querySelector(`#definition_label_${id}`).classList.toggle('hidden');
    document.querySelector(`#definition_input_${id}`).classList.toggle('hidden');
}

//  scripts for loading words 
function loadPage(i) {
    //console.log('loading function loadPage;')
    //console.log('Page number ' + i);
    const url = location.href + '/getWordsToEdit';
    fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                page: i,
                wordsPerPage: 'default'
            })
        })
        .then(response => response.json())
        .then(result => {
            let container = document.querySelector('#wordsContainer');
            container.innerHTML = '';
            result['words'].forEach(word => {
                let div = document.createElement('div');
                // assign class word
                div.classList.add('word');
                div.innerHTML = `
						<span class='term'>
							<span id='term_label_${word['id']}'>${word['term']}</span>
							<input id='term_input_${word['id']}' type='text' class='hidden' value="${word['term']}" />
						</span>
						<span class='definition'>
							<span id='definition_label_${word['id']}'>${word['definition']}</span>
							<input id='definition_input_${word['id']}' type='text' class='hidden' value="${word['definition']}" />
						</span>
						`;
                        /*<span class='icons'>
							
						</span> */

                //<button data-changemode=false data-id=${word['id']} onclick='changeWord(this);'><img src=${pencilIconPath} class="icon" alt="Edit word"></button>


                container.append(div);
                // wordsContainer
            })
        })
}