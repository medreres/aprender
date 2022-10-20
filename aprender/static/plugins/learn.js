
    document.addEventListener('DOMContentLoaded', () => {
        // load words on start
        getWords();
    })

    var idOfWord = 0;
    // number of all words received
    var wordsNumber = 0;

    function toggleNextQuestion(id) {
        let questionOne = document.querySelector(`#id_index${id}`);
        let questionTwo = document.querySelector(`#id_index${id+1}`);
        questionOne.classList.toggle('hidden');
        questionTwo.classList.toggle('hidden');
    }

    function toggleRestartMenu() {

    }

    function restartLearnWay() {
        // path = 
        let path = "{% url 'restartLearnWay' id %}";
        fetch(path)
            .then(response => response.json())
            .then(result => {
                // console.log(result);
                location.reload();
            })
    }

    function toggleRoundMenu() {
        document.querySelector('#learnCardContainer').classList.toggle('hidden');
        document.querySelector('#roundMenu').classList.toggle('hidden');
    }

    function startNewRound() {
        idOfWord = 0;
        wordsNumber = 0;
        document.querySelector('#learnCardContainer').innerHTML = '';
        document.querySelector('#wordsLearned').innerHTML = '';
        toggleRoundMenu();
        getWords();
    }

    function checkAnswer(element) {
        let path = location.href + '/check';
        fetch(path, {
                method: 'POST',
                body: JSON.stringify({
                    'id': element.dataset.id,
                    'definition': element.dataset.definition
                })
            })
            .then(response => response.json())
            .then(result => {
                if (result['answer']) {
                    element.classList.toggle('bg-success');
                } else {
                    element.classList.toggle('bg-danger');
                }
                element.addEventListener('transitionend', () => {
                    setTimeout(() => {
                        if (idOfWord >= wordsNumber - 1) {
                            toggleRoundMenu();
                        } else
                            toggleNextQuestion(idOfWord++);
                    }, 1000);
                });
            })
    }

    function getWords() {

        // if round is over, show menu of words studied

        let path = location.href + '/getWords';
        fetch(path)
            .then(result => result.json())
            .then(response => {

                // if learn way is finished, there is 'finish' key in dictionary
                if ('finish' in response) {
                    document.querySelector('#restartMenu').classList.toggle('hidden');
                    return;
                }

                // save those words to show at the end of the round
                wordsStudied = response['words']

                // create div for eact word-definitnio set
                let wordsContainer = document.querySelector('#learnCardContainer');

                wordsNumber = response['words'].length;
                response['words'].forEach((word, index) => {

                    // console.log(word);

                    let answers = '';
                    word['definitions'].forEach((definition, index) => {
                        let answer =
                            `<button type="button" class="btn btn-primary answer" onclick="checkAnswer(this);" data-id='${word['word']['id']}' data-definition=${definition}>${definition}</button>`;
                        answers += answer;
                    })
                    let divContainer = document.createElement('div');
                    divContainer.classList.add('learn-card');
                    divContainer.id = `id_index${index}`;
                    divContainer.dataset.id = word['word']['id'];
                    divContainer.innerHTML = `<span>Definition</span>
                    <div class='word-container'>
                        <span class='word'>${word['word']['term']}</span>
                        <div class='picture'></div>
                        </div>
                        <div class='definitions'>${answers}</div>`;

                    if (index != 0)
                        divContainer.classList.toggle('hidden');
                    wordsContainer.append(divContainer);
                })
                let wordsLearnedContainer = document.querySelector('#wordsLearned');
                response['words'].forEach(word => {

                    let wordLearned = document.createElement('div');
                    wordLearned.classList.toggle('word');
                    wordLearned.innerHTML = `
                        <span>${word['word']['term']}</span>
                        <span>${word['word']['definition']}</span>
                    `;
                    wordsLearnedContainer.append(wordLearned);
                })

            })
    }
