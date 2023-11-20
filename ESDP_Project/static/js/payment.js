var payments = new cp.CloudPayments({
    language: "ru-RU",
    email: "",
    applePaySupport: false,
    googlePaySupport: false,
    yandexPaySupport: false,
    tinkoffInstallmentSupport: false,
});


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
            payer_postal_code
        }
    }).then(function (data) {
        pay(data['order_id'], parseInt(total), data['account_id'])
    })
}

let pay = function (orderId, total, accountId) {
    payments.pay('charge',
        { //options
            publicId: 'test_api_00000000000000000000002', //id из личного кабинета
            description: 'Оплата товаров в example.com', //назначение
            amount: total, //сумма
            currency: 'KZT', //валюта
            accountId: accountId, //идентификатор плательщика (необязательно)
            invoiceId: orderId, //номер заказа  (необязательно)
            skin: "classic", //дизайн виджета (необязательно)
        }).then(function (widgetResult) {
            console.log('result', widgetResult);
        }).catch(function (error) {
            console.log('error', error);
        }
    )
}
;

$('#checkout').click(order);