from rest_framework import serializers
from .models import Producto, Categoria, Tipo, Pago, Detalle, Metodo, Envio, Region, Comuna, Carrito, Carrito_detalle

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

class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle
        fields = '__all__'

class MetodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodo
        fields = '__all__'

class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = '__all__'

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

class CarritoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito_detalle
        fields = '__all__'
