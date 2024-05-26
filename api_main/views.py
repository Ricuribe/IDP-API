from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Producto, Pedido, Detalle
from .serializers import UserSerializer, RegisterSerializer, ProductoSerializer, PedidoDetalleSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
                'user': RegisterSerializer(user).data,
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