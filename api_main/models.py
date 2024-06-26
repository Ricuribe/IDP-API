import os
import uuid
from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=70)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    tipo = models.ForeignKey('Tipo', on_delete=models.CASCADE)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.TextField(max_length=3000, blank=True, null=False)
    descuento = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(upload_to='img_productos/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        
        if self.imagen:
            ext = self.imagen.name.split('.')[-1]
            filename = f'{uuid.uuid4()}.{ext}'
            while os.path.exists(os.path.join(self.imagen.storage.location, 'img_productos', filename)):
                filename = f'{uuid.uuid4()}.{ext}'
            self.imagen.name = filename
        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_producto} - {self.nombre}"

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id_categoria} - {self.nombre}"

class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id_tipo} - {self.nombre}"

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    metodo = models.ForeignKey('Metodo', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now=True)
    token_transaccion = models.CharField(max_length=64, null=True, blank=True)
    estado_transaccion = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.id_pago} - {self.usuario}"

class Detalle(models.Model):
    pago = models.ForeignKey('Pago', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.pago} - {self.producto}"

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pago = models.ForeignKey('Pago', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.id_pedido} - {self.usuario}"

class Metodo(models.Model):
    id_metodo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    activo = models.BooleanField()

    def __str__(self):
        return f"{self.id_metodo} - {self.nombre}"

class Envio(models.Model):
    id_envio = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pago = models.ForeignKey('Pago', on_delete=models.CASCADE)
    direccion = models.CharField(max_length=50)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)
    estado = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id_envio} - {self.usuario}"

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id_region} - {self.nombre}"

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.id_comuna} - {self.nombre}"

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_carrito} - {self.usuario}"

class Carrito_detalle(models.Model):
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.carrito} - {self.producto}"
