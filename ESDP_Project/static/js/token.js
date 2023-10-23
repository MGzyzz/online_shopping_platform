$('#loginForm').submit(function (event){
    let email = $('#loginEmail').val()
    let password = $('#loginPassword').val()
    let token
    $.ajax({
        url: 'http://localhost:8000/api/login',
        method: 'POST',
        data: {
            username: email,
            password: password
        }
    }).then(function (data){
        token = data.token
        localStorage.setItem('Token', token)
    }).catch(function (error){
        console.log(error)})

})
