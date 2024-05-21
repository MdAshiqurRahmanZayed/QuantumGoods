import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
# To automatically create one to one objects

from django.db.models.signals import post_save
from django.dispatch import receiver


class MyAccountManager(BaseUserManager):
     def create_user(self,email,password=None,username=None):
          if not email:
               raise ValueError('User must have an email address')

          if not username:
               username = email.split('@')[0]+'_'+email.split('@')[1].split('.')[0]
          
          user = self.model(
               email      = self.normalize_email(email),
               username   = username,
          )
          
          user.set_password(password)
          user.save(using=self._db)
          return user
     
     def create_superuser(self,email,password,username=None):
          
          if not username:
               username = email.split('@')[0]+'_'+email.split('@')[1].split('.')[0]
               
          user = self.create_user(
               email      = self.normalize_email(email),
               username   = username,
               password   = password,
          )
          user.is_admin      = True
          user.is_active     = True
          user.is_staff      = True
          user.is_superadmin = True
          user.save(using=self._db)
          return user
          
USER_TYPES = (
     ('buyer', 'Buyer'),
     ('seller', 'Seller'),
)
class Account(AbstractBaseUser,PermissionsMixin):
    username      = models.CharField(max_length=50, unique=True,null=False,blank=True)
    email         = models.EmailField(max_length=100, unique=True)

    #required
    date_joined   = models.DateTimeField(auto_now_add=True)
    last_login    = models.DateTimeField(auto_now_add=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    user_type = models.CharField(verbose_name='User Type', max_length=20, choices=USER_TYPES, default='buyer')
    
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username',]
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
         return self.is_admin
    
    def has_module_perms(self,add_label):
         return True
   
    
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    
    first_name    = models.CharField(max_length=50,null=True,blank=True)
    last_name     = models.CharField(max_length=50,null=True,blank=True)
    phone_number  = models.CharField(max_length=50,null=True,blank=True)
    address_line_1 = models.CharField( max_length=100,null=True,blank=True)
    address_line_2 = models.CharField( max_length=100,null=True,blank=True)
    profile_picture = models.ImageField( upload_to='images/profile',default='default/user.png',null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    zipcode = models.CharField( max_length=20,null=True,blank=True)
    country = models.CharField( max_length=20,null=True,blank=True)

    def __str__(self):
        return self.user.email

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
   
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
   
    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value=='':
                return False
        return True
   
   
@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()