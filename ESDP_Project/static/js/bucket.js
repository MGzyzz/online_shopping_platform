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

function updateQuantity(itemId, newQuantity){
    $.ajax({
        url: `http://localhost:8000/api/bucket/${itemId}/update_quantity/`,
        method: 'PUT',
        data: {
            id: itemId,
            new_quantity: newQuantity
        },
        dataType: 'json',
        success: function (response){
            if (response.success){
                console.log('Quantity updated successfully')
                parseInt($('span[name="' + response.name + '"]').text(response.total_price + ' тг'))
            }
        },
        error: function (response){
            console.log('Error Quantity update',response.error)
        }
    })
}

function incrementQuantity(itemId){
    let quantityInput=$('#quantity-' + itemId)
    let newQuantity = parseInt(quantityInput.val()) + 1
    quantityInput.val(newQuantity)

    updateQuantity(itemId, newQuantity)
}

function decrementQuantity(itemId){
    let quantityInput=$('#quantity-'+itemId)
    let newQuantity = parseInt(quantityInput.val() -1 )

    if (newQuantity >= 1){
        quantityInput.val(newQuantity)
        updateQuantity(itemId, newQuantity)
    }
}
