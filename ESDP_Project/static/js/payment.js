const checkout = new cp.Checkout({
    publicId: 'pk_0992ab759ec4dc1d6119b4d15f1ee',
});
const paymentForm = $('#paymentFormSample');
const cardNumber = $('#card-input');
const expDateMonth =$('#expDateMonth');
const expDateYear = $('#expDateYear');

paymentForm.submit((e) => {
    e.preventDefault();
    checkout.container = document.getElementById('paymentFormSample');
    checkout.createPaymentCryptogram().then((cryptogram) => {
        console.log(cryptogram)
    }).catch((e) => {
        console.log(e)
    })
})



