from django.db import models
from django.contrib.auth.models import User
import PIL.Image

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(null=True, blank=True, max_length=200)


	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY_CHOICES = (
		("Clothes", "Clothes"),
		("Shoes", "Shoes"),
		("Jewelry", "Jewelry"),
		("Cosmetics", "Cosmetics"),
		("Foods", "Foods"),
		("Furnitures", "Furnitures"),
		("Equiptments", "Equiptments"),
		("Books", "Books"),
		("Accessories", "Accessories"),
		("Electronics", "Electronics"),
		("Fashion", "Fashion"),
		("Parts", "Parts"),
	


	)
	name = models.CharField(max_length=200)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, null=True, blank=True)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	digital = models.BooleanField(default=False,null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='products/', default="")

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
	    return str(self.id)


	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total



class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
	

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profileImages", default="avatar.png")
    phoneNumber = models.IntegerField(null=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    profession = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    homeAddress = models.CharField(max_length=200, null=True, blank=True)
    mailingAddress = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField()

    def __str__(self) -> str:
        return f'{self.user.username} Profile'


class Image(models.Model):
 
    image = models.ImageField(upload_to="images", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.image)
        width, height = img.size
        target_width = 600
        h_coefficient = width/600
        target_height = height/h_coefficient
        img = img.resize((int(target_width), int(target_height)), PIL.Image.ANTIALIAS)
        img.save(self.image.path, quality=100)
        img.close()
        self.image.close()



class SubscribedUsers(models.Model):
    email = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)