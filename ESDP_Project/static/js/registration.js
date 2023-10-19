document.addEventListener('DOMContentLoaded', function () {
    let registrationButton = document.getElementById('registrationButton');
    let myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    let smsConfirmInput = document.getElementById('smsConfirm');
    let registrationDoneButton = document.getElementById('registrationDone');

    registrationButton.addEventListener('click', function (event) {
        event.preventDefault();
        if (validateForm()) {
            myModal.show();
        }
    });

    myModal._element.addEventListener('show.bs.modal', function () {
        console.log('open');
    });

    registrationDoneButton.addEventListener('click', function () {
        if (smsConfirmInput.value === '4444') {
            document.getElementById('registrationForm').submit();
        } else {
            alert('Неверный код!');
        }
    });

    smsConfirmInput.addEventListener('input', function () {
        checkSmsConfirmValidity();
    });
});

function checkSmsConfirmValidity() {
    let smsConfirmInput = document.getElementById('smsConfirm');
    let registrationDoneButton = document.getElementById('registrationDone');

    if (smsConfirmInput.value.length === 4) {
        registrationDoneButton.removeAttribute('disabled'); // Активируем кнопку
    } else {
        registrationDoneButton.setAttribute('disabled', 'disabled'); // Деактивируем кнопку
    }
}
function validateForm() {
    let firstName = document.getElementById('inputFirstName').value;
    let lastName = document.getElementById('inputLastName').value;
    let sureName = document.getElementById('inputSurname').value;
    let phone = document.getElementById('inputPhone').value;
    let email = document.getElementById('inputEmail').value;
    let pass1 = document.getElementById('inputPassword').value;
    let pass2 = document.getElementById('inputPasswordConfirm').value;
    let sellerCheck = document.getElementById('inputStatus');

    if (!firstName || !lastName || !sureName || !phone || !email || !pass1 || !pass2 ) {
        alert('Пожалуйста, заполните все поля.');
        return false;
    }
     let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Пожалуйста, введите корректный email.');
        return false;
    }

    // let phoneRegex = /^\d{10}$/; // Например, 1234567890
    // if (!phoneRegex.test(phone)) {
    //     alert('Пожалуйста, введите корректный номер телефона (10 цифр).');
    //     return false;
    // }

    if (pass1 !== pass2) {
    alert('Пароли не совпадают.');
    return false;
    }

    // if (sellerCheck.checked && !confirm('Вы уверены, что являетесь продавцом?')) {
    //     return false;
    // }


    return true;
}

