from django.db import models


class Size(models.Model):
    """sizes of a product"""
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Color(models.Model):
    """colors of a product"""
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Category(models.Model):
    """categories of a product & its subcategories"""
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="subs")
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products", null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.SmallIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="products/")
    size = models.ManyToManyField(Size, related_name="products", null=True, blank=True)
    color = models.ManyToManyField(Color, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.title


class Information(models.Model):
    """additional information about a product"""
    text = models.TextField()
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name="information")

    def __str__(self):
        return self.text[:30]
