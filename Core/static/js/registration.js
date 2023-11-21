document.addEventListener('DOMContentLoaded', function () {

    let registrationButton = $('#registrationButton');
    let myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    let smsConfirmInput = $('#smsConfirm');
    let registrationDoneButton = $('#registrationDone');

    // registrationButton.click(function (event) {
    //     event.preventDefault();
    //     if (validateForm()) {
    //         myModal.show();
    //     }
    // });

    // myModal._element.addEventListener('show.bs.modal', function () {
    //     console.log('open');
    // });
    //
    // registrationDoneButton.click(function () {
    //     if (smsConfirmInput.val() === '4444') {
    //         $('#registrationForm').submit();
    //     } else {
    //         alert('Неверный код!');
    //     }
    // });

    // smsConfirmInput.on('input',function () {
    //     checkSmsConfirmValidity();
    // });
});

function checkSmsConfirmValidity() {
    let smsConfirmInput = $('#smsConfirm');
    let registrationDoneButton = $('#registrationDone');

    if (smsConfirmInput.val().length === 4) {
        registrationDoneButton.prop('disabled', false); // Активируем кнопку
    } else {
        registrationDoneButton.prop('disabled', true); // Деактивируем кнопку
    }
}

function validateForm() {
    let firstName = $('#id_first_name').val();
    let lastName = $('#id_last_name').val();
    let phone = $('#id_phone').val();
    let email = $('#id_email').val();
    let pass1 = $('#id_password1').val();
    let pass2 = $('#id_password2').val();

    if (!firstName || !lastName || !phone || !email || !pass1 || !pass2) {
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

    return true;
}

