from django.contrib.auth.models import BaseUserManager



class EmployeeManager(BaseUserManager):
   
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', 1)
        extra_fields.setdefault('is_staff', 0)
        extra_fields.setdefault('is_superuser', 0)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_active', 1)
        extra_fields.setdefault('is_staff', 1)
        extra_fields.setdefault('is_superuser', 1)

        if extra_fields.get('is_staff') != 1:
            raise ValueError("Superuser must have is_staff=1.")
        if extra_fields.get('is_superuser') != 1:
            raise ValueError("Superuser must have is_superuser=1.")

        return self.create_user(email, password, **extra_fields)
