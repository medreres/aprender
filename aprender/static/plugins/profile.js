// by default load user sets
var profileUsername;

function setUsername() {
    const url = new URL(location.href);
    const username = url.pathname.replace('/', '');
    window.profileUsername = username;
}




document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#setsBtn').addEventListener('click', loadUserSets);
    document.querySelector('#foldersBtn').addEventListener('click', loadUserFolders);
    setUsername();

    loadSets(undefined, profileUsername, 'contentContainer');
})

function loadUserSets(evt) {
    // load posts via ajax
    if (!evt.target.classList.contains('active')) {
        loadSets(undefined, profileUsername, 'contentContainer');
        toggleActive('userSetsLink', ['userSetsLink', 'userFoldersLink']);
    }
}

function loadUserFolders(evt) {
    if (!evt.target.classList.contains('active')) {
        loadFolders(undefined, profileUsername, 'contentContainer');
        toggleActive('userFoldersLink', ['userSetsLink', 'userFoldersLink']);
    }
}