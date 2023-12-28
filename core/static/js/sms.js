$(document).ready(function () {
    $('.otp-card-inputs input').keyup(function (e) {
        if ($(this).val().length == $(this).attr('maxlength') && $(this).next().length) {
            $(this).next('input').focus();
        }
    });
    let userId = $('#userId').val()
    console.log(userId)
    axios.get(`http://sms-service:1026/sms/send/${userId}`)
    .then(function(response){
        console.log(`success ${response.data}`)
    }).catch(function(response) {
        console.log(`fail ${response.data}`)
    })
    .finally(function(response){
    console.log}('request Handled'))
    })
