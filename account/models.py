import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import  Image
from company.models import Company 
import uuid
 



# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    uniq = uuid.uuid1()
    filename = "."+filename.split(".")[-1]
    file_path = 'userprofile/'+str(uniq)+filename
    
    return file_path

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Geçerli bir mail adresini girin!')

        if not username:
            raise ValueError('Geçerli bir kullanıcı adi girin!')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    
    user_type       = models.SmallIntegerField(default=0) ##0::::>upload   1::::>manager  2::::>super
    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin  = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    class Meta:
        db_table = 'user_account'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    address_line_1 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(default='userprofile/default.jpg', upload_to = user_directory_path)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)   
    phone_number = models.CharField(max_length=20, null=True)  
    
    class Meta:
        db_table = 'user_profile'
    
    def __str__(self):
        return self.user.email

    def save(self, *agrs, **kwargs):
        super().save(*agrs, **kwargs)
        if self.profile_picture:
            try:
                img = Image.open(self.profile_picture.path)
                if img.height > 1000 or img.width > 1200:
                    output_size = (983, 983)
                    img.thumbnail(output_size)
                    img.save(self.profile_picture.path)
            except:
                # If the file is not an image, set the profile picture to the default
                os.remove(self.profile_picture.path)
                self.profile_picture = 'userprofile/default.jpg'
                self.save()

 

class UserRight(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True) 
    is_approve = models.BooleanField(default=False)
    is_access = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_right'
    
    def __str__(self):
        return self.name

# class UserAuth(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, default=1)
#     right = models.ForeignKey(UserRight, on_delete=models.CASCADE, default=1)

class UserAuth(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, default=None)
    right = models.ForeignKey(UserRight, on_delete=models.DO_NOTHING, default=None)

    class Meta:
        db_table = 'user_auth'

    def has_no_right(user_id,right):
        """Kullanıcın gönderilen yetki ismine göre kaydı var ise True yok ise False"""
        return not UserAuth.objects.filter(user_id=user_id, right__name=right).exists()
    
    def get_right_id(right):
        """Gönderilen isme göre yetki ID si döndür"""
        return UserAuth.objects.filter(right__name=right).values('right_id')[0]['right_id']

    def __str__(self):
        return f'{self.user.email} {self.right.name}'


    #  try:
    #     user_auth = UserAuth.objects.get(user_id=request.user.id, right__name="store_finance")
    # except UserAuth.DoesNotExist:
    #     context = {
    #     'userprofile': userprofile,
    #     }
    #     return render(request, '403.html',context)
   

     
