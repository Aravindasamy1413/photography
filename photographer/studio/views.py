from django.shortcuts import render, redirect
from .models import Booking
from .forms import FrameOrderForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from .models import FrameOrder
from .models import Gallery
from django.db.models import Q
from django.contrib import messages
from .models import FrameImage

def home(request):
    return render(request, 'home.html')


def booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        event_type = request.POST['event_type']
        date = request.POST['date']
        start_time = request.POST.get('start_time')
        location = request.POST['location']

        Booking.objects.create(
            name=name,
            email=email,
            phone=phone,
            event_type=event_type,
            date=date,
            start_time=start_time,
            location=location
        )
        messages.success(request, "Booking Successfull")
        # 🔥 EMAIL SEND CODE
        subject = 'New Booking Request'
        message = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Event: {event_type}
        Date: {date}
        Start Time: {start_time}                                                                                                                                                                                                                                                                            
        Location: {location}
        """

        print("EMAIL FUNCTION RUNNING 🔥")  # debug

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return redirect('home')

    return render(request, 'booking.html')

def frame_order(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        frame_type = request.POST['frame_type']
        size = request.POST['size']
        caption = request.POST.get('caption')
        address = request.POST['address']

        # 🔥 First create order WITHOUT photo
        order = FrameOrder.objects.create(
            name=name,
            email=email,
            phone=phone,
            frame_type=frame_type,
            size=size,
            caption=caption,
            address=address
        )

        # 🔥 Multiple images
        images = request.FILES.getlist('photos')
        for img in images:
            FrameImage.objects.create(order=order, image=img)

        messages.success(request, "Frame Order Successful ✅")

        # 🔥 Email
        email_msg = EmailMessage(
            subject='New Frame Order 📸',
            body=f"""
Name: {name}
Email: {email}
Phone: {phone}
Frame Type: {frame_type}
Size: {size}
Caption: {caption}
Address: {address}
""",
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
        )

        # 🔥 Attach all images
        for img in order.images.all():
            email_msg.attach_file(img.image.path)

        email_msg.send()

        return redirect('home')

    return render(request, 'frame_order.html')

def gallery(request):
    category = request.GET.get('category')

    if category == "Wedding":
        photos = Gallery.objects.filter(
            Q(category__icontains="wedding") |
            Q(category__icontains="reception")
        )
    elif category:
        photos = Gallery.objects.filter(category__icontains=category)
    else:
        photos = Gallery.objects.all()

    return render(request, 'gallery.html', {'photos': photos})



def contact(request):
    return render(request, 'contact.html')



#tracking order

def track_order(request):
    order = None

    if request.method == "POST":
        phone = request.POST.get('phone')

        order = FrameOrder.objects.filter(phone=phone).last()

        if not order:
            messages.error(request, "❌ No order found for this phone number")

    return render(request, 'track.html', {'order': order})