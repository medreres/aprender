let editToggle = false;

let popoverTriggerList, popoverList;
document.addEventListener('DOMContentLoaded', () => {
    popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
})

async function editFolderName(body) {
    const folderId = location.href.substring(location.href.lastIndexOf('/') + 1);
    const path = `${folderId}/edit`;

    fetch(path, {
            method: 'POST',
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(result => {
            //    console.log(result);
            // return result;
        })
}

async function toggleEdit() {

    let buttons = document.querySelectorAll('button[name=cardDelete]');
    buttons.forEach(button => button.classList.toggle("hidden"));

    let label = document.querySelector('#label');
    label.classList.toggle('hidden');

    let labelInput = document.querySelector('#labelInput');
    labelInput.classList.toggle('hidden');

    let description = document.querySelector('#description');
    description.classList.toggle('hidden');

    let descriptionInput = document.querySelector('#descriptionInput');
    descriptionInput.classList.toggle('hidden');

    if (editToggle) {
        let body = {};

        if (descriptionInput.value != description.innerHTML) {
            body['description'] = descriptionInput.value;
            description.innerHTML = descriptionInput.value;
        }

        if (labelInput.value != label.innerHTML) {
            body['label'] = labelInput.value;
            label.innerHTML = labelInput.value;
        }
        if (Object.keys(body).length) {
            // console.log('changed! Making fetch request')
            const response = await editFolderName(body);
            // console.log(response);

        }
    }



    editToggle = !editToggle;
    // console.log('ending of function');
}



function deleteSet(element, evt) {
    evt.preventDefault();
    const path = `${location.href}/addSet`;
    const setId = element.dataset.id;
    const folderId = location.href.substring(location.href.lastIndexOf('/') + 1);
    fetch(path, {
            method: 'POST',
            body: JSON.stringify({
                setId: setId,
                folderId: folderId
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(`#set_${setId}`)
            document.querySelector(`#set_${setId}`).remove();
        })
}