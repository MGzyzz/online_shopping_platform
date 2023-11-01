// function getCSRFToken() {
//     let cookies = document.cookie.split(';');
//     for (let i = 0; i < cookies.length; i++) {
//         let cookie = cookies[i].trim();
//         if (cookie.indexOf('csrftoken=') === 0) {
//             return cookie.substring('csrftoken='.length, cookie.length);
//         }
//     }
//     return null;
// }

// console.log("===", getCSRFToken())

function toCart() {
    $('.cart-btn').click(function (event){
        event.preventDefault();
        let productId = $(this).data('product-id');

        $.ajax({
            url: 'http://127.0.0.1:8000/api/bucket/add_to_cart/',
            type: 'POST',
            data: {
                product: productId,
                quantity: 1,
            },
            success: function (response){
                console.log('Product added', response)
            },
            error: function (error){
                console.log('fail',error)
            }
        })
    })
}

function toCartUser() {
    $('.cart-btn-user').click(function (event){
        event.preventDefault();
        let productId = $(this).data('product-id');
        let userId = $(this).data('user-id')

        $.ajax({
            url: 'http://127.0.0.1:8000/api/bucket/add_to_cart/',
            type: 'POST',

            data: {
                product: productId,
                quantity: 1,
                user: userId

            },
            success: function (response){
                console.log('Product added', response)
            },
            error: function (error){
                console.log('fail',error)
            }
        })
    })
}

toCartUser()

toCart()