from django.db import models

# Create your models here.

class Review(models.Model):
	title = models.CharField(max_length=50)
	content = models.CharField(max_length=120)
	author = models.ForeignKey('account.Profile', on_delete=models.CASCADE, default=None)
	def __repr__(self):
		return f"Review: {self.id}, {self.title}"

class Product(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(max_length=300)
	price = models.FloatField(null=True)
	image = models.ImageField(default='products/default.jpg', upload_to='products')
	stock = models.PositiveIntegerField()
	is_in_stock = models.BooleanField(default=True)

	def __repr__(self):
		return f"Product: {self.id}, {self.title}"
