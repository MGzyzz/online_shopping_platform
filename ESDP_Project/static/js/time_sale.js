let startDateInp = $('#start_date')
let endDateInp = $('#end_date')
let token = localStorage.getItem('Token')

let now = new Date()
let currentDate = now.toISOString().slice(0,16)
let productId = $('#product').val()
startDateInp.attr('min', currentDate)
endDateInp.attr('min', currentDate)
let addBtn = $('.add-discount')

checkSale(productId)

addBtn.click(function (){
    $('#exampleModal').show()
})



$('#make_sale').click(function () {
        let startDate = startDateInp.val()
        let endDate = endDateInp.val()
        let product = $('#product').val()
        let discount = $('#percent').val()

        $.ajax({
            url: `http://localhost:8000/api/time_discount/`,
            method: "POST",
            data: {
                product: product,
                start_date: startDate,
                end_date: endDate,
                discount: discount,
            },
            headers: {
                'Authentication': `Token ${token}`
            }

        }).then(function (){
            $('#exampleModal').hide()
            let discountBtn =  $('.add-discount')
            discountBtn.hide()
            $('#delete-btn').show()
        })

})

$('#delete-btn').click(function (){
    let productId = $('#product').val()
    getSaleId(productId).then(function (data) {
            let discountId = data.discount_id
            if (discountId) {
                $('#delete_modal').show()
            } else {
                alert('Скидка не найдена для данного продукта.')
            }
        })
})

function getSaleId (productId) {
     return $.ajax({
            url: `http://localhost:8000/api/time_discount/get-discount-by-product/?product_id=${productId}`,
            method: 'GET',
            headers: {
                'Authentication': `Token ${token}`
            }
        })
}

$('#delete_sale').click(function (){
    let productId = $('#product').val()

        getSaleId(productId).then(function (data) {
            let discountId = data.discount_id
            if (discountId) {
                $.ajax({
                    url: `http://localhost:8000/api/time_discount/${discountId}/`,
                    method: "DELETE",
                    headers: {
                        'Authentication': `Token ${token}`
                    }
                }).then(function () {
                    $('#delete_modal').hide()
                    $('#delete-btn').hide()
                    $('.add-discount').show()
                })
            } else {
                alert('Скидка не найдена для данного продукта.')
            }
        })
})

$('.close-btn').click(function (){
     $('#exampleModal').hide()
    $('#delete_modal').hide()
})

function checkSale(productId){
    getSaleId(productId).then(function (data) {
            let discountId = data.discount_id
            if (discountId) {
                $.ajax({
                    url: `http://localhost:8000/api/time_discount/${discountId}/check-expiration/`,
                    method: 'GET',
                    headers: {
                        'Authentication': `Token ${token}`
                    },
                }).then(function (data){
                    if (data.expired) {
                        $('#delete-btn').hide()
                        $('.add-discount').show()
                    }
                    else {
                        $('#delete-btn').show()
                        $('.add-discount').hide()
                    }
                })
            } else {
                alert('Скидка не найдена для данного продукта.')
            }
        })
}

setInterval(function (){
    let productId = $('#product').val()
    checkSale(productId)
}, 10000)