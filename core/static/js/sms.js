$(document).ready(function () {
    $('.otp-card-inputs input').keyup(function (e) {
        if ($(this).val().length == $(this).attr('maxlength') && $(this).next().length) {
            $(this).next('input').focus();
        }
    });

    let userId = $('#userId').val();
    console.log(userId);

    axios.post(`http://172.19.0.1:1026/sms/send/${userId}`)
        .then(function (response) {
            console.log(`success`, response);
        })
        .catch(function (error) {
            console.log(`fail`, error);
        });
});
