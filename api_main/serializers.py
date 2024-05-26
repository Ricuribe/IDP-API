from rest_framework import serializers
from .models import Producto, Categoria, Tipo, Pago, Detalle, Metodo, Envio, Region, Comuna, Carrito, Carrito_detalle, Pedido
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'categoria', 'tipo', 'precio','stock', 'descuento', 'descripcion', 'imagen', 'imagen_url']

    def get_imagen_url(self, obj):
        if obj.imagen:
            return obj.imagen.url
        return None

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
        read_only_fields = ['usuario']

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle
        fields = '__all__'

class MetodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodo
        fields = '__all__'
        

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        Fields = '__all__'

class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = '__all__'
        read_only_fields = ['usuario']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'
        read_only_fields = ['usuario']

class CarritoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito_detalle
        fields = '__all__'

# Api view serializers
class ProductoDetalleSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='producto.nombre')
    cantidad = serializers.IntegerField()

    class Meta:
        model = Detalle
        fields = ['producto', 'nombre', 'cantidad']

class PedidoDetalleSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'usuario', 'fecha', 'estado', 'productos']
        read_only_fields = ['id_pedido', 'usuario', 'fecha', 'productos']

    def get_productos(self, obj):
        detalles = Detalle.objects.filter(id_pago=obj.pago)
        return ProductoDetalleSerializer(detalles, many=True).data