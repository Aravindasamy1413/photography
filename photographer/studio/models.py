from django.db import models

# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    event_type = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
class FrameOrder(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    photo = models.ImageField(upload_to='frames/', blank=True, null=True)

    frame_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    address = models.TextField()

    caption = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=200, default='Pending')

    def __str__(self):
        return self.name

class FrameImage(models.Model):
    order = models.ForeignKey(FrameOrder,on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='frames/')

    def __str__(self):
        return f"Image for {self.order.name}"
    
class Gallery(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title