document.addEventListener("DOMContentLoaded", () => {
    let setsButton = document.querySelector("#setsButton");

    setsButton.addEventListener('click', (evt) => {
        evt.stopPropagation();
        loadSets(evt);
        hideLink();
    });

    let foldersButton = document.querySelector("#foldersButton");
    foldersButton.addEventListener('click', (evt) => {
        evt.stopPropagation();
        loadSets(evt);
        hideLink();
    });
    document.querySelector('#libraryBtn').addEventListener('click', loadSets);
})

function loadSets(event) {
    fetch("{% url 'fetchsets' request.user %}")
        .then(response => response.json())
        .then(result => {
            if (result.length === 0) {
                addCard(undefined);
            } else {
                result.forEach(card => addCard(card));
            }
        })
}

function addCard(card) {

    if (card === undefined) {
        document.querySelector('#containerAjax').innerHTML =
            "It's seem that there is nothing to show!";
        return;
    }
    document.querySelector('#containerAjax').innerHTML = "";

    setTimeout(() => {
        let tmp = `
                                    <div class="card">
                                    <div class="card-header">
                                        ${card['label']}
                                    </div>
                                    <div class="card-body">
                                        ${card['wordsNumber']} words
                                    </div>
                                    </div>
                                    `;

        document.querySelector('#containerAjax').innerHTML += tmp;
    }, 1)


}

function loadFolders(event) {
    // event.stopPropagation();


    // document.querySelector('#setsButton').classList.toggle('active');
    // event.target.classList.toggle('active');
    // hideLink();
}

function hideLink() {
    // toggle classes for css
    document.querySelector('#foldersLink').classList.toggle('hidden');
    document.querySelector('#setsLink').classList.toggle('hidden');

    // toggle visibilyty for a links
    document.querySelector('#foldersButton').classList.toggle('active');
    document.querySelector('#setsButton').classList.toggle('active');
}