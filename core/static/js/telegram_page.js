const shopData = window.location.href.split('?')[1]
const parsedShopData = JSON.parse(decodeURIComponent(shopData));

const shopDataContainer = document.getElementById('shopDataContainer')
shopDataContainer.images.forEach(image =>{
shopDataContainer.innerHtml='
    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src=`${image}` class="d-block w-100" alt="...">
    </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>'})
shopDataContainer.innerHTML = '
</div>
    <div class="card-body text-center">
        <h5 class="card-title">${parsedShopData.name}</h5>
        <p class="card-text text-center">Цена: ${parsedShopData.price}</p>
        <p class="cart-text text-center"> ${parsedShopData.description}</p>
        <a href="#" class="btn btn-primary text-center">Заказать</a>
    </div>
'