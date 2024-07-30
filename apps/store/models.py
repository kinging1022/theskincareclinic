from django.db import models
from django.utils.text import slugify 
from PIL import Image
from io import BytesIO
from django.core.files import File

# Create your models here.

class Category(models.Model):
    parent= models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=225)
    slug = models.CharField(max_length=225,unique=True, blank=True)
    ordering = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self) -> str:
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)





class BrandCategory(models.Model):
    image = models.ImageField(upload_to='uploads/',blank=True, null=True)
    title = models.CharField(max_length=225)
    slug = models.CharField(max_length=225,unique=True, blank=True)
    ordering = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = 'BrandCategories'
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    brand = models.ForeignKey(BrandCategory,related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('self', related_name = 'variants', on_delete= models.CASCADE, blank=True, null=True )
    title = models.CharField(max_length=225)
    slug = models.CharField(max_length=225,unique=True, blank=True)
    is_featured = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visits = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)



    class Meta:
        ordering = ('-date_added',)


    def __str__(self) -> str:
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
            else:
                return ''
    
    
    
    
    
    def make_thumbnail(self,image, size=(100,100)):
        img =   Image.open(image)

        if img.mode == 'RGBA':
            img = img.convert('RGB')

        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail



class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete= models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/',blank=True, null=True)


    def __str__(self) -> str:
        return self.product.title
    
    
            
    def save(self, *args, **kwargs):
        
        if self.image:
            self.thumbnail = self.make_thumbnail(self.image)
        
        super().save(*args, **kwargs)
    
    
    
    
    
    def make_thumbnail(self,image, size=(100,100)):
        img =   Image.open(image)

        if img.mode == 'RGBA':
            img = img.convert('RGB')

        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail