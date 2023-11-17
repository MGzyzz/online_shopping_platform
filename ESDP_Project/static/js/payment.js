const checkout = new cp.Checkout({
    publicId: 'pk_0992ab759ec4dc1d6119b4d15f1ee',
});
const paymentForm = $('#paymentFormSample');
const cardNumber = $('#card-input');
const expDateMonth = $('#expDateMonth');
const expDateYear = $('#expDateYear');

paymentForm.submit((e) => {
    e.preventDefault();
    checkout.container = $('#paymentFormSample');
    checkout.createPaymentCryptogram().then((cryptogram) => {
        console.log(cryptogram)
    }).catch((e) => {
        console.log(e)
    })
})

cardNumber.on('input', formatAndValidateCreditCardNumber)
cardNumber.on('blur', lunh_validate)

expDateMonth.on('input', FormatDateMonth)
expDateMonth.on('blur', ValidateDateMonth)

function formatAndValidateCreditCardNumber() {
    const number = cardNumber.val().replace(/\D/g, '');
    let formattedNumber = '';

    for (let i = 0; i < number.length; i++) {
        if (i > 0 && i % 4 === 0) {
            formattedNumber += ' ';
        }
        formattedNumber += number[i];
    }

    const isValid = formattedNumber.length >= 19;
    $('#pay-btn').prop('disabled', !isValid);
    cardNumber.val(formattedNumber);

}

function lunh_validate() {
    const number = cardNumber.val().replace(/\D/g, '');
    let sum = 0, len = number.length, parity = len % 2;
    for (let i = 0; i < len; i++) {
        let digit = parseInt(number[i]);
        if (i % 2 === parity) {
            digit *= 2;
            if (digit > 9) {
                digit -= 9;
            }
        }
        sum += digit;

    }
    if (sum % 10 !== 0) {
        $('#pay-btn').prop('disabled', true);
        $('#cardError').text('Некорректный номер карты').addClass('text-danger');
        cardNumber.addClass('border border-danger');
    } else {
        $('#pay-btn').prop('disabled', false);
        $('#cardError').text('Номер карты').removeClass('text-danger');
        cardNumber.removeClass('border border-danger');
    }

}

function FormatDateMonth() {
    const number = expDateMonth.val().replace(/\D/g, '');
    if (number.length > 2) {
        expDateMonth.val(number.substring(0, 2));
    }

}

function ValidateDateMonth() {
    const number = expDateMonth.val().replace(/\D/g, '');
    const min = 1;
    const max = 12;
    if (number < min || number > max) {
        $('#pay-btn').prop('disabled', true);
        $('#expDateMonthError').text('Неверный месяц').addClass('text-danger');
        expDateMonth.addClass('border border-danger');
    } else {
        $('#pay-btn').prop('disabled', false);
        $('#expDateMonthError').text('Месяц').removeClass('text-danger');
        expDateMonth.removeClass('border border-danger');
    }
}
