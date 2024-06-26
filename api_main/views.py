from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Carrito, Carrito_detalle, Metodo, Pago, Producto, Pedido, Detalle
from .serializers import UserSerializer, RegisterSerializer, ProductoSerializer, PedidoDetalleSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .webpay_config import webpay_config
from transbank.error.transbank_error import TransbankError
from django.http import HttpResponseRedirect
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType

webpay_config()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response(status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class IndexNewProductosView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        productos = Producto.objects.order_by('-id_producto')[:9] 
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

class PedidoDetalleView(APIView):

    def get(self, request, id_pedido):
        pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
        serializer = PedidoDetalleSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id_pedido):
        pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
        new_estado = request.data.get('estado')

        if new_estado is None:
            return Response({'error': 'Estado no proporcionado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        pedido.estado = new_estado
        pedido.save()

        detalles = Detalle.objects.filter(id_pago=pedido.pago)
        for detalle in detalles:
            producto = detalle.producto
            producto.stock -= detalle.cantidad
            producto.save()

        serializer = PedidoDetalleSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id_pedido):
        pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
        new_estado = request.data.get('estado')

        if new_estado is None:
            return Response({'error': 'Estado no proporcionado.'}, status=status.HTTP_400_BAD_REQUEST)

        pedido.estado = new_estado
        pedido.save()

        serializer = PedidoDetalleSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        id_producto = request.data.get('id_producto')
        cantidad = request.data.get('cantidad', 1)
        print("1 ", request.user, "\n 2", request.data)
        
        if not id_producto:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            producto = Producto.objects.get(id_producto=id_producto)
        except Producto.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Carrito.objects.get_or_create(usuario=user)
        
        cart_item, created = Carrito_detalle.objects.get_or_create(carrito=cart, producto=producto, cantidad=cantidad)
        if not created:
            cart_item.cantidad += cantidad
            cart_item.save()
            return Response({"message": "Quantity changed"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)


class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]  # Asegura que el usuario esté autenticado

    def post(self, request):
        amount = request.data 
        
        pago = Pago.objects.create(
            usuario=request.user,
            metodo= Metodo.objects.get(pk = 1)
        )
        
        buy_order = 'orden_' + str(pago.id_pago)
        session_id = 'session_' + str(pago.id_pago)
        return_url = 'http://localhost:8000/api/return_transaction/'  
        
        try:
            
            print("uhmmm")
            response = Transaction.create(
            IntegrationType.TEST,
            buy_order=buy_order,
            session_id=session_id,
            amount=amount,
            return_url=return_url
            )
            print("wait what")
            
            pago.token_transaccion = response['token']
            pago.estado_transaccion = 'initiated'
            
            pago.save()
            
            return Response({
                'url': response['url'],
                'token': response['token']
            })
        except TransbankError as e:
            return Response({'error': str(e)}, status=500)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
        except KeyError as e:
            print("Error: La respuesta no contiene las claves esperadas: " + str(e))
        

class PaymentReturnView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get('token_ws')

        try:
            
            Transaction = webpay_config()
            result = Transaction.commit( IntegrationType.TEST ,token=token)
            
            print(result)
            
            pago = Pago.objects.get(token_transaccion=token)
            if result['response_code'] == 0 and result['status'] == 'AUTHORIZED':
                pago.estado_transaccion = 'completed'
                
                carrito = Carrito.objects.get(usuario=pago.usuario)
                detalles_carrito = Carrito_detalle.objects.filter(carrito=carrito)
                for item in detalles_carrito:
                    Detalle.objects.create(
                        pago=pago,
                        producto=item.producto,
                        cantidad=item.cantidad
                    )
                    
                    item.producto.stock -= item.cantidad
                    item.producto.save()
                
                detalles_carrito.delete(carrito = carrito)
                
                
            else:
                pago.estado_transaccion = 'failed'
            pago.save()
            
            
            return HttpResponseRedirect(f'http://localhost:4200/payment-result/{pago.estado_transaccion}')
        
        except Exception as e:
            
            return Response({'error': 'An error occurred while processing your payment: ' + str(e)}, status=500)