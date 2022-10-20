
    // const url = new URL(window.location.href);
    // const username = '{{user}}';

    // by default load user sets
    loadSets(undefined, username, 'contentContainer');


    document.addEventListener('DOMContentLoaded', () => {
        document.querySelector('#setsBtn').addEventListener('click', loadUserSets);
        document.querySelector('#foldersBtn').addEventListener('click', loadUserFolders);
    })

    function loadUserSets(evt) {
        // load posts via ajax
        if (!evt.target.classList.contains('active')) {
            loadSets(undefined, username, 'contentContainer');
            toggleActive('userSetsLink', ['userSetsLink','userFoldersLink']);
        }
    }

    function loadUserFolders(evt) {
        if (!evt.target.classList.contains('active')) {
            loadFolders(undefined, username, 'contentContainer');
            toggleActive('userFoldersLink', ['userSetsLink','userFoldersLink']);
        }
    }

