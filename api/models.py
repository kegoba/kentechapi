from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    username = None
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField("email", max_length=30, unique = True)
    wallet = models.DecimalField("wallet", max_digits=10, null=True, decimal_places=2)
    phone = models.CharField("phone number",unique=True, null=True,  max_length=15)
    date_joined = models.DateTimeField("date join", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class BankTansfer(models.Model):
    tranaction_id  = models.AutoField(primary_key=True)
    transaction_type = models.CharField("transaction type",null=True, max_length=100)
    description = models.CharField("description", max_length=100)
    sender = models.CharField("sender", max_length=100)
    transaction_amount = models.CharField("tranaction amount", max_length=100)
    transaction_time = models.DateTimeField("date transacted", auto_now_add=True)
    user_id = models.ForeignKey(CustomUser, null=True, related_name="transaction_id", on_delete=models.CASCADE)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_order = models.CharField("Cart Item", null=True,  max_length=1000)
    date_order = models.DateTimeField("date join", auto_now_add=True)
    total_price = models.DecimalField("price of product", max_digits=10, null=True, decimal_places=2)
    user_id = models.ForeignKey(CustomUser, null=True, related_name="order_id", on_delete=models.CASCADE)





class Vtu_transaction(models.Model):
    vtu_id  = models.AutoField(primary_key=True)
    transaction_type = models.CharField("transaction type",null=True, max_length=100)
    amount = models.DecimalField("amout", max_digits=10, null=True, decimal_places=2)
    ref_id = models.CharField("reference number", max_length=100)
    phone = models.CharField("phone number credited", null=True, max_length=100)
    transaction_time = models.CharField("transaction time", null=True,  max_length=100)
    user_id = models.ForeignKey(CustomUser, null=True, related_name="vtu_id", on_delete=models.CASCADE)
    



class Product (models.Model):
    product_id = models.AutoField(primary_key=True)
    product_price = models.DecimalField("price of product", max_digits=10, null=True, decimal_places=2)
    product_category = models.CharField("list of Catergories", null=True, max_length=100)
    image = models.ImageField("image", upload_to='post_images' , null=True)
    product_desc = models.CharField("product description", null=True, max_length=100)



class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True,on_delete=models.CASCADE)
    item = models.CharField("Cart Item", null=True,  max_length=1000)
    user_id = models.ForeignKey(CustomUser, null=True, related_name="cart_id", on_delete=models.CASCADE)