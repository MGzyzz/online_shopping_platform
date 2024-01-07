$(document).ready(function () {
    $('.otp-card-inputs input').keyup(function (e) {
        if ($(this).val().length == $(this).attr('maxlength') && $(this).next().length) {
            $(this).next('input').focus();
        }
    });
    let userId = $('#userId').val()
    let isRequestSent = localStorage.getItem('isRequestSent')
    if (!isRequestSent){
    $.ajax({
        url: `http://sms:1026/sms/send/${userId}`,
        method: 'POST',
        success: function (resp){
            console.log(`success ${resp}`)
            // localStorage.setItem('isRequestSent', true)
        },
        error: function (err) {
            console.log(`fail ${err}`)
        }
})}
});



