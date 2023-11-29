function order() {
    let products = $('#cart-products').val()
    let shop = $('#shop').val()
    let total = $('#form-total').val()
    let payer_name = $('#id_payer_name').val()
    let payer_surname = $('#id_payer_surname').val()
    let payer_phone = $('#id_payer_phone').val()
    let payer_email = $('#id_payer_email').val()
    let payer_address = $('#id_payer_address').val()
    let payer_city = $('#id_payer_city').val()
    let payer_postal_code = $('#id_payer_postal_code').val()
    let account = $('#user-id').val()
    $.ajax({
        url: 'http://localhost:8000/api/order/create_order/',
        method: 'POST',
        data: {
            products,
            shop,
            total,
            payer_name,
            payer_surname,
            payer_phone,
            payer_email,
            payer_address,
            payer_city,
            payer_postal_code,
            account
        }
    }).then(function (data) {
        pay(data['order_id'], parseFloat(total), payer_phone, data['user_id'])
    })
}

let pay = function (orderId, total, payer_phone, account) {
        var widget = new cp.CloudPayments();
        widget.pay('charge',
            { //options
                publicId: 'pk_3d2e6006deeae8feba63160d9efd2', //id из личного кабинета
                description: 'Оплата товаров в example.com', //назначение
                amount: total, //сумма
                currency: 'KZT', //валюта
                accountId: account, //идентификатор плательщика (необязательно)
                invoiceId: orderId, //номер заказа  (необязательно)
                skin: "classic", //дизайн виджета (необязательно)б
                payer: {
                    phone: payer_phone, //номер телефона плательщика
                }
            }).then(function (widgetResult) {
            console.log('result', widgetResult);
            window.location.reload()
        }).catch(function (error) {
                console.log('error', error);
            }
        )

    }
;

$('#checkout').click(order);