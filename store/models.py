from django.db import models

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=100)
    discount =models.FloatField()

class Collection(models.Model):
    search = models.CharField(max_length=200)
    featured_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')
class Product(models.Model):
    unit_title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) #auto_now will automatically save the current d/t field
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['lastname','firstname'])
        ]

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS =[
        (PAYMENT_PENDING,'Pending'),
        (PAYMENT_COMPLETE,'Complete'),
        (PAYMENT_FAILED,'Failed')
    ]
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    #customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10,blank=True)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()