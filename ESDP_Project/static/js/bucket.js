function toCart() {
    $('.cart-btn').click(function (event){
        event.preventDefault();
        let productId = $(this).data('product-id');

        $.ajax({
            url: 'http://localhost:8000/api/bucket/add_to_cart/',
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
            url: 'http://localhost:8000/api/bucket/add_to_cart/',
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

function deleteFromBucket(){
    $('.delete-from-bucket').click(function (event){
        event.preventDefault()
        let itemId = $(this).data('item-id')
        $.ajax(
            {
                url: `http://localhost:8000/api/bucket/${itemId}/remove_from_cart/`,
                type: 'DELETE',
                success: function (response){
                    console.log('Successful deleted',response)
                },
                error: function (error){
                    console.log('Error', error)
                }

            }

        )
    })
}

deleteFromBucket()
toCartUser()

toCart()