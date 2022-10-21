function checkResults(form) {
    const data = new FormData(form);
    // console.log(data.getAll('np'))
    return false;
}

var numberOfWordsCorrect = 0;
var currentWord = 0;

// add id for all questions to parse them easier and hides all words
function addIndexes() {
    document.querySelectorAll('.learn-card').forEach((element, index) => {
        if (index != 0)
            element.classList.add('hidden');
        element.id = `id_${index}`;
    })
}

document.addEventListener('DOMContentLoaded', () => {
    addIndexes();
})


function checkAnswer(element) {
    const url = new URL(location.href);
    let path = url.origin + '/sets/' + setId + '/learn/check';
    // console.log(element.value)
    // console.log(path);
    fetch(path, {
            method: 'POST',
            body: JSON.stringify({
                'id': element.dataset.id,
                'definition': element.value
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result['answer'] === true) {
                element.classList.toggle('correct');
                // console.log('correct');
                numberOfWordsCorrect++;
            } else {
                // console.log('incorrect');
                element.classList.toggle('incorrect');
            }


            setTimeout(() => {
                if (currentWord != numberOfWordsGeneral - 1) {
                    toggleNextDiv(currentWord);
                    toggleNextDiv(currentWord + 1);
                    currentWord++;
                } else {
                    toggleFinishMenu();
                }
            }, 2000)
        })
}

function toggleNextDiv(id) {
    document.querySelector(`#id_${id}`).classList.toggle('hidden');
}

function toggleFinishMenu() {
    document.querySelector('#result').style.display = 'flex';
    document.querySelector('#wordsSection').classList.toggle('hidden');
    let percent = 100 * numberOfWordsCorrect / numberOfWordsGeneral;
    console.log(percent);
    console.log(`${percent}%`);
    document.querySelector('#percents').innerHTML = `${percent}%`;
    document.querySelector('#percents').style.width = `${percent}%`;
}


function checkWord(evt) {
    if (evt.name === 'written') {
        disable(evt);
        // console.log(`input[name="written"] [data-id="${evt.dataset.id}"]`)
        let definition = document.querySelector(`input[name="written"][data-id="${evt.dataset.id}"]`);
        // console.log(definition);
        checkAnswer(definition);
    } else if (evt.name === 'multiple') {
        document.querySelectorAll(`input[name="multiple"][data-id="${evt.dataset.id}"]`).forEach(element => element
            .classList.toggle('disabled'))
        checkAnswer(evt);
    } else if (evt.name === 'true') {
        // console.log(evt.value);
        document.querySelectorAll(`button[name="true"][data-id="${evt.dataset.id}"]`).forEach(element => element
            .classList.toggle('disabled'))
        checkAnswer(evt);
    }
}

function disable(element) {
    element.disabled = true;
}