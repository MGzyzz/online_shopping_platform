$(document).ready(function () {
    $('.otp-card-inputs input').keyup(function (e) {
        if ($(this).val().length == $(this).attr('maxlength') && $(this).next().length) {
            $(this).next('input').focus();
        }
    });
    let userId = $('#userId').val()
    console.log(userId)
    $.ajax({
        url: `https://market.shopuchet.kz/sms/send/${userId}`,
        method: 'POST',
        success: function (resp){
            console.log(`success ${resp}`)
        },
        error: function (err) {
            console.log(`fail ${err}`)
        }
})
});
