from celery import shared_task
from django.core.mail import send_mail
from Auth.models import LoginUser

@shared_task()
def send_event_mail(title,link,starts,end,user_id,recipient):
    user=LoginUser.objects.get(id=user_id)
    starts=starts.strftime("%Y/%m/%d %H:%M %p")
    end=end.strftime("%Y/%m/%d %H:%M %p")
    BODY=f"<p>Hey there, <br><br>A new <strong>Event</strong> has been created.</p><br>Here are the details of this Event:<br><br>Title: {title}<br>Starts: {starts}<br>Ends: {end}<br>Host: {user.first_name} {user.last_name}<br>Link: {link}<br><br><br>Regards,<br>Slam"
    send_mail("Event Created","","Slam <alerts@slamapp.co>",[recipient],html_message=BODY,fail_silently=True)
    