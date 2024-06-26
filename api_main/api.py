from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Producto, Categoria, Tipo, Pago, Detalle, Metodo, Envio, Region, Comuna, Carrito, Carrito_detalle, Pedido
from .serializers import ProductoSerializer, CategoriaSerializer, TipoSerializer, PagoSerializer, DetalleSerializer, MetodoSerializer, EnvioSerializer, RegionSerializer, ComunaSerializer, CarritoSerializer, CarritoDetalleSerializer, PedidoSerializer
from .permissions import DynamicModelPermissions
from api_main import permissions

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), DynamicModelPermissions()] 
    
    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria = self.request.query_params.get('categoria')
        
        if categoria:
            queryset = queryset.filter(categoria__id_categoria__icontains=categoria)
        
        return queryset

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), DynamicModelPermissions()]

class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), DynamicModelPermissions()]

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [DynamicModelPermissions]
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class DetalleViewSet(viewsets.ModelViewSet):
    queryset = Detalle.objects.all()
    serializer_class = DetalleSerializer
    permission_classes = [DynamicModelPermissions]

class MetodoViewSet(viewsets.ModelViewSet):
    queryset = Metodo.objects.all()
    serializer_class = MetodoSerializer
    permission_classes = [DynamicModelPermissions]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), DynamicModelPermissions()]

class ComunaViewSet(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), DynamicModelPermissions()]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    def get_queryset(self):
        queryset = Carrito.objects.all()
        usuario = self.request.query_params.get('usuario')
        
        if usuario:
            queryset = queryset.filter(usuario__id__icontains=usuario)
            
        return queryset

class CarritoDetalleViewSet(viewsets.ModelViewSet):
    queryset = Carrito_detalle.objects.all()
    serializer_class = CarritoDetalleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Carrito_detalle.objects.all()
        carrito = self.request.query_params.get('carrito')
        
        if carrito:
            queryset = queryset.filter(carrito__id_carrito__icontains=carrito)
            
        return queryset
