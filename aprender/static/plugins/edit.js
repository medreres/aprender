// for assigning id for divs with words
var id = 1;

// saving interval
const SAVEPAUSE = 300000;


// set id


// store all words in json
var words = []

function addField() {
    let termContainer = document.querySelector('#wordsContainer');
    termContainer.append(createField())
    document.querySelector(`#term_input_${id-1}`).focus();
    // toggleInput(id - 1);
    return false;
}

function deleteWord(element) {
    //make post query to change the word in database
    let div = document.querySelector(`div[id=word_${element.id}]`)
    let dataId = div.dataset.id;
    // console.log(dataId)
    // if word is freshly added and hasn't been saved, then its not in database yet
    console.log(dataId)
    console.log(words);
    wordToDelete = words.find(word => word['id'] == dataId);
    console.log(wordToDelete)
    if (wordToDelete && wordToDelete['status'] != 'add') {
        const url = new URL(location.href);
        const path = `${url.origin}/sets/${setId}/deleteWord`;
        fetch(path, {
                method: "POST",
                body: JSON.stringify({
                    id: dataId
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            })
    } else {
        console.log('freshly added')
    }
    // delete from word array
    words.splice(words.indexOf(wordToDelete), 1)
    div.remove();
}

function createField() {


    let div = document.createElement('div');
    // assign class word
    div.classList.add('word');
    div.id = `word_${id}`;
    div.dataset.id = id;
    div.innerHTML = `
                    <span class='term'>
                    <span class='id'>#${id}</span>
                        <input  id='term_input_${id}' type='text'  value=''
                        oninput="changeWord(this, ${id})";
                        />
                    </span>
                    <span class='definition'>
                        <input id='definition_input_${id}' type='text'  value=''
                        oninput="changeWord(this, ${id})";
                        />
                        
                    </span>
                    <span class='icons'>
                        <button tabindex="-1" onclick='deleteWord(this);' id=${id} data-id=${id}><img src=${deleteIconPath} class="icon" alt="Delete word"></button>
                    </span>
                    `;
    id++;


    return div;
}

function changeWord(element, id) {
    // console.log(element, id);
    wordToChange = words.find(word => word['id'] === id);
    if (typeof (wordToChange) == 'undefined') {
        wordToChange = {
            'id': id,
            'term': '',
            'definition': '',
            'status': 'add'
        }
        words.push(wordToChange)
    } else if (wordToChange['status'] != 'add') {
        wordToChange['status'] = 'change';
    }
    // console.log('before ');
    // console.log(wordToChange)

    if (element.id.includes('term')) {
        wordToChange['term'] = element.value;
    } else {
        wordToChange['definition'] = element.value;
    }

    // console.log('after ')
    // console.log(wordToChange)
}

function saveWord(id) {
    let term = document.querySelector(`#term_input_${id}`).value;
    let definition = document.querySelector(`#definition_input_${id}`).value;

    console.log(term, definition);

    document.querySelector(`#term_label_${id}`).innerHTML = term;
    document.querySelector(`#definition_label_${id}`).innerHTML = definition;

    //make post query to change the word in database
    const url = new URL(location.href);
    const path = `${url.origin}/sets/${setId}/saveChanges`;
    fetch(path, {
            method: 'POST',
            body: JSON.stringify({
                id: id,
                term: term,
                definition: definition
            })
        })
        .then(response => response.json())
        .then(result => {
            if ('id' in result) {
                console.log('word saved')
                //document.querySelectorAll(`.icons > button[dataset-id=${id}`).forEach(element => element.dataset.id = result['id'])

            }
        })
}


var termDefinitionNode;
document.addEventListener('DOMContentLoaded', () => {
    loadWords();
    termDefinitionNode = document.querySelector('.word');
})


// autosave every 5 min
function autoSave() {

    saveChanges();
    setTimeout(() => {
        document.querySelector('#saveHeader').classList.toggle('hidden');
        setTimeout(() => {
            document.querySelector('#saveHeader').classList.toggle('hidden');
        }, 2000);
    }, 2000);
    setTimeout(autoSave, SAVEPAUSE);
}

setTimeout(() => {
    autoSave();
}, SAVEPAUSE)

function saveChanges() {
    fetch('saveChanges', {
            method: 'PATCH',
            body: JSON.stringify({
                words: words,
                label: document.querySelector('#setLabel').value,
                description: document.querySelector('#setDescription').value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })


}

function submitForm() {
    saveChanges();
    const url = setPath;
    window.location.href = url;

}

function loadWords() {
    const url = new URL(location.href);
    const path = `${url.origin}/sets/${setId}/getWordsToEdit`;
    fetch(path, {
            method: 'POST',
            body: JSON.stringify({
                wordsPerPage: 'all'
            })
        })
        .then(response => response.json())
        .then(result => {
            let container = document.querySelector('#wordsContainer');


            // set label and descripiton
            document.querySelector('#setDescription').value = result['description'];
            document.querySelector('#setLabel').value = result['label'];

            container.innerHTML = '';
            result['words'].forEach((word) => {
                //TODO word has 3 status: initial, change, add
                word['status'] = 'initial';
                words.push(word);
                let div = document.createElement('div');
                // assign class word
                div.classList.add('word');
                div.id = `word_${id}`;
                div.dataset.id = word['id']
                div.innerHTML = `
                    <span class='term'>
                    <span class='id'>#${id}</span>
                    
                        <input id='term_input_${word['id']}' type='text' value="${word['term']}" 
                        oninput="changeWord(this, ${word['id']})";
                        />
                    </span>
                    <span class='definition'>
                        <input id='definition_input_${word['id']}' type='text'  value="${word['definition']}" 
                        oninput="changeWord(this, ${word['id']})";
                        />
                    </span>
                    <span class='icons'>
                        <button tabindex="-1" onclick='deleteWord(this);' id=${id} dataset-id=${word['id']}><img src="${deleteIconPath}" class="icon" alt="Delete word"></button>
                    </span>
                    `;

                id++;

                container.append(div);
                
            })
        })
}