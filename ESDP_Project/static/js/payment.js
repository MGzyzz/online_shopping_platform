const checkout = new cp.Checkout({
    publicId: 'pk_0992ab759ec4dc1d6119b4d15f1ee',
});
const paymentForm = $('#paymentFormSample');
const cardNumber = $('#card-input');
const expDateMonth =$('#expDateMonth');
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

cardNumber.on('input',formatAndValidateCreditCardNumber)
cardNumber.on('blur',lunh_validate)

function formatAndValidateCreditCardNumber(){
    const number = cardNumber.val().replace(/\D/g, '');
    let formattedNumber = '';

    for (let i = 0; i < number.length; i++) {
        if (i>0 && i%4 === 0) {
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
    console.log(sum)
    if (sum % 10 !== 0) {
        $('#pay-btn').prop('disabled', true);
        $('#cardError').text('Некорректный номер карты').addClass('text-danger');
        $('#card-input').addClass('border border-danger');
    }

}

