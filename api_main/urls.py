from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AddToCartView, IndexNewProductosView, LoginView, RegisterView, UserDetailView, LogoutView, PedidoDetalleView, CreateTransactionView, PaymentReturnView
from .api import ProductoViewSet, CategoriaViewSet, TipoViewSet, PagoViewSet, DetalleViewSet, MetodoViewSet, EnvioViewSet, RegionViewSet, ComunaViewSet, CarritoViewSet, CarritoDetalleViewSet, PedidoViewSet


router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'tipos', TipoViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'detalles', DetalleViewSet)
router.register(r'metodos', MetodoViewSet)
router.register(r'envios', EnvioViewSet)
router.register(r'regiones', RegionViewSet)
router.register(r'comunas', ComunaViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'carritos-detalles', CarritoDetalleViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/', UserDetailView.as_view(), name='user-detail'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('productos/nuevos/', IndexNewProductosView.as_view(), name='index_new_productos'),
    path('pedidos/<int:id_pedido>/', PedidoDetalleView.as_view(), name='pedido-detalle'),
    path('add-to-cart/', AddToCartView.as_view(), name='agregar-carro'),
    path('create_transaction/', CreateTransactionView.as_view(), name='create_transaction'),
    path('return_transaction/', PaymentReturnView.as_view(), name='return_transaction')
]
