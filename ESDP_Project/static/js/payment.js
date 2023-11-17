var payments = new cp.CloudPayments({
    language: "ru-RU",
    email: "",
    applePaySupport: false,
    googlePaySupport: false,
    yandexPaySupport: false,
    tinkoffInstallmentSupport: false,
});


this.pay = function () {
    payments.pay('charge',
        { //options
            publicId: 'test_api_00000000000000000000002', //id из личного кабинета
            description: 'Оплата товаров в example.com', //назначение
            amount: 100, //сумма
            currency: 'KZT', //валюта
            accountId: 'user@example.com', //идентификатор плательщика (необязательно)
            invoiceId: '1234567', //номер заказа  (необязательно)
            email: 'user@example.com', //email плательщика (необязательно)
            skin: "classic", //дизайн виджета (необязательно)
            data: {
                myProp: 'myProp value'
            },
        }).then(function (widgetResult) {
            console.log('result', widgetResult);
        }).catch(function (error) {
            console.log('error', error);
        }
    )
}
;

$('#checkout').click(pay);