from rest_framework.views import APIView,Response
from rest_framework import status,viewsets
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class UserRegView(APIView):
    def post(self,request):
        serializer=Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
               { "message":"Registered Successfully"}
               ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        try:
            user=Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response(
            {"message":"Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
            )
        if check_password(password,user.password):
            refresh = RefreshToken()
            refresh["user_id"] = user.id
            return Response(
                {
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
        )
        

        return Response(
            {"message": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class AdminloginView(APIView):
    def post(self,request):
        serializer=AdminLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        username=serializer.validated_data["username"]
        password=serializer.validated_data["password"]

        user=authenticate(username=username,
                          password=password)
        if user is not None and user.is_superuser:
            refresh=RefreshToken.for_user(user)
            return Response(
                {
                    "message":"Admin login successful",
                    "refresh":str(refresh),
                    "access":str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "error":"Invalid username or password"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )




class ProductViewSet(viewsets.ModelViewSet):
   # permission_classes=[IsAuthenticated]
    queryset=Product.objects.prefetch_related("images")
    serializer_class=ProductSerializer
    parser_classes=[
        MultiPartParser,
        FormParser,
    ]

    def create(self,request,*args,**kwargs):

        product=Product.objects.create(
            name=request.data.get("name"),
            description=request.data.get("description",""),
            price=request.data.get("price")
        )

        images=request.FILES.getlist("images")

        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image
            )

        serializer=self.get_serializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self,request,*args,**kwargs):
        product=self.get_object()

        product.name=request.data.get("name",product.name)

        product.description=request.data.get(
            "description",product.description)

        product.price=request.data.get(
            "price",product.price
        )

        product.save()

        images=request.FILES.getlist("images")

        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image
            )

        serializer=self.get_serializer(product)

        return Response(serializer.data)


class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.prefetch_related("images")
        serializer = ProductSerializer(products, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CartView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        cart,create=Cart.objects.get_or_create(user=user)
        serializer=CartSerializer(cart)

        return Response(serializer.data,status=status.HTTP_200_OK)
        
    
    def post(self, request):
        product = Product.objects.get(id=request.data.get("product"))
        user=request.user
        cart,create = Cart.objects.get_or_create(user=user)
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=request.data.get("quantity")
        )

        return Response(
            {"message": "Added to cart"},
            status=status.HTTP_201_CREATED
        )



class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = Cart.objects.get(user=user)
        order = Order.objects.create(user=user,total_amount=0,status="Pending")
        total = 0

        for item in cart.items.all():
            OrderItem.objects.create(order=order,
                                     product=item.product,
                                     quantity=item.quantity,
                                     price=item.product.price)
            total += item.product.price * item.quantity

        order.total_amount = total
        order.save()

        return Response(
            {"message": "Order placed successfully"},
            status=status.HTTP_201_CREATED
        )

    def get(self, request):

        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserLogoutView(APIView):

    def post(self, request):
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )



class AdminUserView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):

        users = Users.objects.all()

        serializer = AdminUserSerializer(users, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class AdminOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):

        orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class SellingView(APIView):

    def get(self, request):

        orders = Order.objects.all()
        total_orders = orders.count()
        total_sales = sum(order.total_amount for order in orders)
        total_products = sum(
            item.quantity
            for order in orders
            for item in order.items.all()
        )

        return Response({
            "total_orders": total_orders,
            "total_sales": total_sales,
            "total_products_sold": total_products
        })

    

class AdminLogoutView(APIView):

    def post(self, request):

        

        return Response(
            {"message": "Admin logout successful"},
            status=status.HTTP_200_OK
        )