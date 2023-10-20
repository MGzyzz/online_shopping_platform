let startDateInp = $('#start_date')
let endDateInp = $('#end_date')
let csrfToken = $("input[name='csrfmiddlewaretoken']").val();

let now = new Date()
let currentDate = now.toISOString().slice(0,16)

startDateInp.attr('min', currentDate)
endDateInp.attr('min', currentDate)

$('.add-discount').click(function (){
    $('#exampleModal').show()
})



$('#make_sale').click(function (event) {
        event.preventDefault()
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
                csrfmiddlewaretoken: csrfToken
            },
        }).then(function (){
            $('#exampleModal').hide()
            let discountBtn =  $('.add-discount')
            discountBtn.text('Убрать скидку')
            discountBtn.addClass('btn-danger')
        })

})

$('.close-btn').click(function (){
     $('#exampleModal').hide()
})
