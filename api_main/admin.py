from django.contrib import admin
from .models import *

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Pago)
admin.site.register(Detalle)
admin.site.register(Metodo)
admin.site.register(Envio)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Carrito)
admin.site.register(Carrito_detalle)