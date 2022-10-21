const tabs = ['setsButton', 'foldersButton', 'favorite'];
const links = ['setsLink', 'foldersLink', 'favoritesLink'];
// to make absolute url instead of relative
let url = new URL(location.href);
let path = url.origin;

function detectClickSets() {
    let setsButton = document.querySelector("#setsButton");
    setsButton.addEventListener('click', (evt) => {
        evt.stopPropagation();
        loadSets(evt);

        // toggleActive('setsButton', 'foldersButton');
        toggleActive('setsButton', tabs);
        // 
        toggleLink('setsLink', links);
    });
}

function detectClickFolders() {
    let foldersButton = document.querySelector("#foldersButton");
    foldersButton.addEventListener('click', (evt) => {
        evt.stopPropagation();
        loadFolders(evt);

        // toggleActive('setsButton', 'foldersButton');
        toggleActive('foldersButton', tabs);
        toggleLink('foldersLink', links);
    });
}

function detectClickFavorite() {
    let favoriteButton = document.querySelector('#favorite');
    favoriteButton.addEventListener('click', (evt) => {
        evt.stopPropagation();
        loadFavoriteSets(evt);

        toggleActive('favorite', tabs);
        toggleLink('favoritesLink', links);
    })
}

function loadFavoriteSets(event, username = window.username, id = 'containerAjax') {
    if (username == undefined) {
        const path = location.href;
        const url = new URL(path);
        const username = url.href.substring(url.href.lastIndexOf('/') + 1);
        // console.log(username);
    } else {
        // console.log(username);
        // console.log('check')
    }
    // console.log(url.origin + '/' + username + '/favorite')
    fetch(url.origin + '/' + username + '/favorite')
        .then(response => response.json())
        .then(result => {
            if (result['set'].length == 0) {
                addCard(undefined);
            }
            result['set'].forEach(element => addCard(element, id))
            // console.log(result);
        })
}

function loadSets(event, username = window.username, id = 'containerAjax', addToFolder = false) {

    const folderId = location.href.substring(location.href.lastIndexOf('/') + 1);
    // console.log(`${path}/${username}/fetchSetsAjax`)
    fetch(`${path}/${username}/fetchSetsAjax`, {
            method: 'POST',
            body: JSON.stringify({
                addToFolder: addToFolder,
                folderId: folderId
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.length === 0) {
                addCard(undefined, id);
            } else {

                if (addToFolder) {
                    const folderId = location.href.substring(location.href.lastIndexOf('/') + 1);
                    fetch(`${path}/folders/${folderId}/getSetsId`, {
                            method: 'POST',
                            body: JSON.stringify({
                                folderId: folderId
                            })
                        })
                        .then(response => response.json())
                        .then(response => {
                            result.forEach(card => addCard(card, id, addToFolder, response['setId']));
                        })
                } else
                    result.forEach(card => addCard(card, id, addToFolder));
            }
        })
}

function addCard(card, id = 'containerAjax', addToFolder = false, setInFolderId) {

    if (card === undefined) {
        document.querySelector(`#${id}`).innerHTML =
            "It's seem that there is nothing to show!";
        return;
    }
    document.querySelector(`#${id}`).innerHTML = "";
    const numberOfEntities = ('wordsNumber' in card) ? `${card['wordsNumber']} words` :
        `${card['setsNumber']} sets`
    let template = document.createElement('div');
    template.classList.add('card');
    template.classList.add('w-100');
    template.innerHTML = `
    
    <div class="card-header">
                ${card['label']}
            </div>
            <div class="card-body">
                ${numberOfEntities}
            </div>`;
    if (!addToFolder) {
        template.onclick = () => {
            // provide location of the set/folder to reroute on click
            // define if it's a set or a folder
            if ('setsNumber' in card) {
                location.href = `${path}/folders/${card['id']}`;
            } else {
                location.href = `${path}/sets/${card['id']}`;
            }
        }
    } else {
        const folderId = location.href.substring(location.href.lastIndexOf('/') + 1);
        // check if set already in folder, accrodingly process click on card, add when is not in folder, remove when is in the on
        if (setInFolderId.some(e => e.id == card['id'])) {
            // console.log(card['id'] + 'already exists')
            template.classList.toggle('included');
        }

        template.onclick = () => {
            // make fetch query to add this set to folder

            // console.log(folderId)
            // console.log('adding to folder!', card['id'])
            const path = `${location.href}/addSet`;
            fetch(path, {
                    method: 'POST',
                    body: JSON.stringify({
                        folderId: folderId,
                        setId: card['id']
                    })
                })
                .then(response => response.json())
                .then(result => {
                    // console.log(result);
                    template.classList.toggle('included');
                    if (template.classList.contains('included')) {
                        toggleCard(card, false)
                    } else {
                        toggleCard(card, true);
                    }
                })
        }

    }


    setTimeout(() => {
        document.querySelector(`#${id}`).append(template);
    }, 1)
}

function toggleCard(element, remove) {
    let folderContainer = document.querySelector('#folderContainer');
    // console.log(element['id']);
    if (remove) {
        document.querySelector(`#set_${element['id']}`).remove();
    } else {
        const url = new URL(location.href);
        const path = url.origin + '/sets';
        // <a class='set' href="${path}/${element['id']}" id="set_${element['id']}">
        //             <div class='set-info'>
        //                 <span>
        //                     <span> ${element['label']}</span>
        //                     <span style='display: block; margin-top: -.5em;'>${element['wordsNumber']} terms</span>
        //                 </span>
        //                 <img class='set-icon' src='${imageIconPath}' alt="set icon">
        //                 <button name="cardDelete" type="button" class="btn btn-primary hidden" data-id='${element['id']}'
        //             onclick="deleteSet(this, event);"><img src="${binIconPath}"
        //                 alt="delete set from folder"></button>
        //             </div>
        //             <div style=''>
        //                 <img src='${userIconPath}' alt="Author profile icon">
        //                 <span>${element['author']}</span>
        //             </div>
        //         </a>
        console.log('loaded carad')
        let set = `
        <div class="card"  onclick=getToSet(this) id="set_${element['id']}" data-id="${element['id']}">
            <div class="card-header">
            ${element['label']}
            </div>
            <div class="card-body">
                <h5 class="card-title">${element['author']}</h5>
                <p class="card-text">${element['wordsNumber']} terms</p>
            </div>
        </div>
                
                
                `;
        // add card
        // let div = document.createElement('div');
        // div.classList.add('folder');
        set.id = `set_${element['id']}`;
        set.innerHTML = element['label'];
        folderContainer.innerHTML += set;
    }
}

function getToSet(element) {
    // when click on div reroute to that sewr page
    location.href = `${path}/sets/${element.dataset.id}`

}


function loadFolders(event, username = window.username, id = 'containerAjax') {

    let url = new URL(location.href);
    let path = url.origin;
    // console.log(`${path}/${username}/fetchFoldersAjax`)
    fetch(`${path}/${username}/fetchFoldersAjax`)
        .then(response => response.json())
        .then(result => {
            if (result.length === 0) {
                addCard(undefined, id);
                return;
            } else {
                result.forEach(card => addCard(card, id))
            }
        })
}

function toggleActive(id, tabs) {


    tabs.forEach(tab => document.querySelector(`#${tab}`).classList.remove('active'))
    document.querySelector(`#${id}`).classList.add('active');
    // console.log(a1,a2);
    // toggle classes for css
    // ids.forEach(id => {
    //     document.querySelector(`#${id}`).classList.toggle('active');
    // })
}

function toggleLink(id, links) {
    // console.log(id)
    links.forEach(link => document.querySelector(`#${link}`).classList.add('hidden'))

    // console.log(document.querySelector(`#${id}`))
    document.querySelector(`#${id}`).classList.remove('hidden');

    // ids.forEach(id => {
    //     document.querySelector(`#${id}`).classList.toggle('hidden');
    // })
}