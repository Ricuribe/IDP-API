from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api import ProductoViewSet, CategoriaViewSet, TipoViewSet, PagoViewSet, DetalleViewSet, MetodoViewSet, EnvioViewSet, RegionViewSet, ComunaViewSet, CarritoViewSet, CarritoDetalleViewSet


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

urlpatterns = [
    path('api/', include(router.urls)),
]
