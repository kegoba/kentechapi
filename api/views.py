from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings


from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import CustomUser, Product, Cart
from .appserializers import RegisterSerializer, Productserializer,Cartserializer

@api_view(["GET", "POST"])
def Home(request):
    user  = CustomUser.objects.all()
    data = RegisterSerializer(user, many=True)
    return Response( data.data,status=status.HTTP_200_OK)
   


@api_view(["POST"])
def RegisterUser(request):
    if request.method == "POST":
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = make_password(request.data.get('password'))
        print("hass password", password)
        phone = request.data.get('phone')
        user_info = {
            "first_name":  first_name,
            "last_name": last_name,
            "email":  email,
            "password":  password, 
            'phone'  : phone
        }
        register = RegisterSerializer(data=user_info)
        try:
            if register.is_valid():
                register.save()
                return Response(
                    register.data,
                    status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    register.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                    )

        except:
            return Response(
                {"message": "email already"}, 
                status=status.HTTP_400_BAD_REQUEST
                )

#VIEW TO LOGIN USER
class C_Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs)->  None :
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user and check_password(password, user.password):
                #CREATING NEW TOKEN AFTER PASSWORD AUTHENTICATION
                token, created = Token.objects.get_or_create(user=user)
                return Response(data={
                    "user_id": user.user_id,
                    "email" : user.email,
                    'last_name' : user.last_name ,
                    " first_name " : user.first_name,
                    " phone" : user.phone,
                    'message': "Login Successful",
                    'status': status.HTTP_200_OK,
                    "token": token.key
                    
                     })
            else:
                return Response(
                {"message":"wrong password or email" },
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            return Response(
                {"message":"Unknown_user"},
                status=status.HTTP_400_BAD_REQUEST
            )


#VIEW THAT WILL DELETE TOKEN AND LOG USER OUT
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Logout_User(request)->  None :

    request.user.auth_token.delete()

    logout(request)

    return Response(data={"message": "logout successful"})



class Add_product(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            product = Productserializer(data=request.data)
            if product.is_valid():
                product.save()
                return Response(product.data, status= status.HTTP_200_OK)
            return Response(product.errors, status= status.HTTP_400_BAD_REQUEST)

        elif request.method == "GET":
            get_product = Product.objects.all()
            product = Productserializer(get_product, many=True)
            return Response(product.data, status= status.HTTP_200_OK)
        return Response(product.errors, status= status.HTTP_400_BAD_REQUEST)
        
        



@api_view(["GET"])
def Get_all_product( request):
    if request.method == "GET":
        get_product = Product.objects.all()
        product = Productserializer(get_product, many=True)
        return Response(product.data, status= status.HTTP_200_OK)
    return Response(product.errors, status= status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def Get_one_product (request,id):
    print(id)
    if request.method == "GET":
        get_product = Product.objects.filter(product_id=id)
        product = Productserializer(get_product, many=True)
        return Response(product.data, status= status.HTTP_200_OK)
    return Response(product.errors, status= status.HTTP_400_BAD_REQUEST)

    


@api_view(["POST"])
def Add_to_cart(request, id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        item, created = Cart.objects.get_or_create(product=product, 
                                                        user=request.user)
        item.quantity += 1
        item.save()
        items = Cartserializer(item, many=True)

        return Response(items.data, status= status.HTTP_200_OK)
    return Response(items.errors, status= status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def Get_all_cart(request):
    if request.method == "GET":
        cart_items = CartItem.objects.filter(user=request.user_id)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        cart_details = {
            'cart_items': cart_items,
            'total_price': total_price
            }
        items = Cartserializer(cart_details, many=True)
        return Response(items.data, status= status.HTTP_200_OK)
    return Response(items.errors, status= status.HTTP_400_BAD_REQUEST)
   

@api_view(["DELETE"])
def remove_from_cart(request,id):
    if request.method =="DELETE":
        cart_item = CartItem.objects.get(id=id)
        cart_item.delete()
        data ={
            "message" : "item deleted successfully"
        }
    return Response(data)


'''
def product_list(request):
    products = Product.objects.all()
    return render(request, 'myapp/index.html', {'products': products})
 
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'myapp/cart.html', {'cart_items': cart_items, 'total_price': total_price})
 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                       user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')


'''