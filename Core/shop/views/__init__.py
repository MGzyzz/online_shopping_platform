from .shop import ShopCreateView, ShopListView, ShopUpdateView, ShopDeleteView, ShopMainView
from .product import ProductCreateView, ProductListView, DetailProduct, EditProduct, DeleteProduct, ShopProductView
from .attributes import AttributesCreateView, AttributesUpdateView
from .profile import Profile
from .order import BucketListView, OrderListView, ShopOrderListView
from .pay import Pay
from .additional_functions import get_client_ip