function toCart() {
    $('.cart-btn').click(function (event){
        event.preventDefault();
        let productId = $(this).data('product-id');

        $.ajax({
            url: 'http://127.0.0.1:8000/api/bucket/add_to_cart/',
            type: 'POST',
            data: {
                product: productId,
                quantity: 1
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

toCart()