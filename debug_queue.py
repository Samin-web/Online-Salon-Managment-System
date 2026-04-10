from django.contrib.auth import get_user_model
from apps.salons.models import Receptionist
from apps.bookings.models import Appointment
from django.utils import timezone


def debug():
    user = get_user_model().objects.get(username='lovely')
    salon = Receptionist.objects.get(user=user).salon
    queue_qs = Appointment.objects.filter(salon=salon, status__in=['pending','confirmed']).order_by('appointment_date','appointment_time')
    queue_items=[]
    for appt in queue_qs:
        services_str = ", ".join([s.name for s in appt.services.all()])
        queue_items.append({
            'token': appt.queue_number or f"T-{appt.id}",
            'customer_name': appt.customer.get_full_name() or appt.customer.username,
            'customer_email': appt.customer.email,
            'service': services_str,
            'staff_name': appt.staff.name if appt.staff else "Unassigned",
            'payment_status': appt.get_payment_status_display(),
            'status': appt.status,
            'appointment_time': appt.appointment_time.strftime('%I:%M %p') if appt.appointment_time else 'Not set',
            'appointment_date': appt.appointment_date.strftime('%M %d, %Y'),
            'total_price': float(appt.final_price or appt.total_price),
            'id': appt.id
        })
    print(queue_items)

# automatically run when imported
if __name__ == '__main__':
    debug()
