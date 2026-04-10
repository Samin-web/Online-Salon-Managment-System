import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import transaction, connection

def test_delete_user(user_id):
    try:
        target_user = User.objects.get(id=user_id)
        print(f"Attempting to delete user: {target_user.username}")
        
        # Use transaction to ensure all deletions happen atomically
        with transaction.atomic():
            # Delete all related objects in the correct order
            from apps.bookings.models import Appointment
            from apps.customers.models import PaymentSubmission
            from apps.salons.models import Review, BlockedCustomer, PromotionBanner, Coupon, Staff, Receptionist
            
            # 1. Handle Legacy/Zombie Tables first (Manually via SQL to avoid IntegrityErrors)
            with connection.cursor() as cursor:
                # Delete appointments from legacy table
                cursor.execute("DELETE FROM booking_appointment WHERE customer_id = %s", [user_id])
                # Delete reviews from legacy table
                cursor.execute("DELETE FROM salon_review WHERE customer_id = %s", [user_id])
                # Delete review replies from legacy table
                cursor.execute("DELETE FROM salon_reviewreply WHERE owner_id = %s", [user_id])
                # Delete complaints from legacy table
                cursor.execute("DELETE FROM salon_complaint WHERE user_id = %s", [user_id])
                # Delete blocked records from legacy table
                cursor.execute("DELETE FROM salon_blockedcustomer WHERE customer_id = %s", [user_id])
                # Delete staff profiles from legacy table
                cursor.execute("DELETE FROM salon_staff WHERE user_id = %s", [user_id])
                
                # Delete service categories and services that reference salons owned by the user
                cursor.execute("""
                    DELETE sc FROM salon_servicecategory sc 
                    INNER JOIN salon_salon s ON sc.salon_id = s.id 
                    WHERE s.owner_id = %s
                """, [user_id])
                cursor.execute("""
                    DELETE ss FROM salon_salonservice ss 
                    INNER JOIN salon_salon s ON ss.salon_id = s.id 
                    WHERE s.owner_id = %s
                """, [user_id])
                
                # Delete salon gallery
                cursor.execute("""
                    DELETE sg FROM salon_salongallery sg 
                    INNER JOIN salon_salon s ON sg.salon_id = s.id 
                    WHERE s.owner_id = %s
                """, [user_id])
                
                # Delete coupons and promotion banners
                cursor.execute("""
                    DELETE c FROM salon_coupon c 
                    INNER JOIN salon_salon s ON c.salon_id = s.id 
                    WHERE s.owner_id = %s
                """, [user_id])
                cursor.execute("""
                    DELETE pb FROM salon_promotionbanner pb 
                    INNER JOIN salon_salon s ON pb.salon_id = s.id 
                    WHERE s.owner_id = %s
                """, [user_id])
                
                # Delete billing invoices
                cursor.execute("""
                    DELETE bi FROM billing_invoice bi 
                    INNER JOIN salon_salon s ON bi.salon_id = s.id 
                    WHERE s.owner_id = %s
                """, [user_id])
                
                # Temporarily disable foreign key checks to handle legacy table deletions
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                # Delete salons from legacy table
                cursor.execute("DELETE FROM salon_salon WHERE owner_id = %s", [user_id])
                # Re-enable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            # 2. Handle Current App Models (Django will handle standard cascades)
            from apps.salons.models import ServiceCategory, SalonService, SalonGallery
            
            # Delete service categories and services that belong to user's salons
            ServiceCategory.objects.filter(salon__owner=target_user).delete()
            SalonService.objects.filter(salon__owner=target_user).delete()
            
            # Delete salon gallery
            SalonGallery.objects.filter(salon__owner=target_user).delete()
            
            # Delete appointments
            Appointment.objects.filter(customer=target_user).delete()
            
            # Delete payment submissions
            PaymentSubmission.objects.filter(customer=target_user).delete()
            
            # Delete reviews
            Review.objects.filter(customer=target_user).delete()
            
            # Delete review replies
            from apps.salons.models import ReviewReply, Complaint
            ReviewReply.objects.filter(owner=target_user).delete()
            
            # Delete complaints
            Complaint.objects.filter(user=target_user).delete()
            
            # Delete blocked customer records
            BlockedCustomer.objects.filter(customer=target_user).delete()
            
            # Delete promotion banners
            PromotionBanner.objects.filter(salon__owner=target_user).delete()
            
            # Delete coupons
            Coupon.objects.filter(salon__owner=target_user).delete()
            
            # Delete user profile
            from apps.accounts.models import Profile
            Profile.objects.filter(user=target_user).delete()
            
            # Delete staff and receptionist profiles
            Staff.objects.filter(user=target_user).delete()
            Receptionist.objects.filter(user=target_user).delete()
            
            # Finally delete the user
            target_user.delete()
            
        print("User deletion successful!")
        return True
        
    except Exception as e:
        print(f"User deletion failed: {e}")
        return False

# Test with user 4
test_delete_user(4)