
    // used to make an instantiation of term-definition container to make copies of it
    var termDefinitionNode;
    // global variable for creating new term-definitions container, used to identify input fields
    var id = 1;
    document.addEventListener('DOMContentLoaded', () => {
        // crate instance of term-definition node
        termDefinitionNode = document.querySelector('.term-definition');
        // id for term-definition input fields
    })

    function addField() {
        let termContainer = document.querySelector('#termDefinitionContainer');
        termContainer.append(createField())
        return false;
    }

    function createField() {
        // make deep copy of node
        let termDefinitionNodeCopy = termDefinitionNode.cloneNode(true);

        // change IDs appropriately, clean input 
        let termField = termDefinitionNodeCopy.querySelector('#term_0');
        termField.id = `term_${id}`;
        termDefinitionNodeCopy.querySelector('#id').innerHTML = id;
        termField.value = '';
        termField.required = '';

        let definitionField = termDefinitionNodeCopy.querySelector('#definition_0');
        definitionField.id = `definition_${id}`;
        definitionField.value = '';
        definitionField.required = '';

        termDefinitionNodeCopy.id = id;

        // increment id for next possible fields
        id++;


        // create cross-sign button to delete if not needed
        let crossSign = document.createElement('span');
        let crossIcon = document.createElement('img');
        // add src and click event to delete 
        crossIcon.src = crossIconPath;
        crossIcon.classList.add('closeBtn');
        crossSign.append(crossIcon);
        termDefinitionNodeCopy.querySelector('.card-header').append(crossSign);
        crossSign.onclick = () => {
            termDefinitionNodeCopy.remove();
        }

        // return ready to use node
        return termDefinitionNodeCopy;
    }
