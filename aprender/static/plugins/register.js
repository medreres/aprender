document.addEventListener('DOMContentLoaded', () => {
    // validate username input
    let usernameInput = document.querySelector('#id_username');
    if (usernameInput.value) {
        validateUsername(usernameInput);
    }
    usernameInput.addEventListener('blur', () => validateUsername(usernameInput))

    // validate email input
    let emailInput = document.querySelector('#id_email');
    if (emailInput.value) {
        emailValid(emailInput);
    }
    emailInput.addEventListener('blur', () => emailValid(emailInput));

    // validate password input
    let passwordInput = document.querySelector('#id_password');
    let passwordInput1 = document.querySelector('#id_password_confirm');

    if (passwordInput1.value) {
        validatePassword(passwordInput, passwordInput1);
    }
    passwordInput1.addEventListener('blur', () => {
        
        validatePassword(passwordInput, passwordInput1)
    });
    passwordInput.addEventListener('blur', () => {

        validatePassword(passwordInput, passwordInput1)
    });


    document.addEventListener('submit', (evt) => {
        if (!(validateForm(evt.target))) {
            evt.preventDefault();
        }
    })


})

function emailValid(element) {
    if (validateEmail(element.value)) {
        toggleValid(element);
    } else {
        toggleInvalid(element);
    }
}

function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function validateForm(form) {
    let isValid = true;
    form.querySelectorAll('input').forEach(input => {
        if (input.classList.contains('is-invalid')) {
            isValid = false;
        }
    })

    return isValid;
}

function validatePassword(element, element1) {
    if (element.value != element1.value) {
        toggleInvalid(element);
        toggleInvalid(element1);
    } else {
        toggleValid(element);
        toggleValid(element1);
    }
}

function toggleValid(element) {
    element.classList.add('is-valid');
    element.classList.remove('is-invalid');
}

function toggleInvalid(element) {
    element.classList.remove('is-valid');
    element.classList.add('is-invalid');
}

function validateUsername(element) {

    let username = element.value;
    const path = location.href + '/username_available';
    fetch(path, {
            method: 'POST',
            body: JSON.stringify({
                username: username
            })
        })
        .then(response => response.json())
        .then(result => {
            if ('error' in result) {
                toggleInvalid(element);
            } else {
                toggleValid(element);
            }
        })
}