from django.db import models

from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

import tagulous.models
import select2.fields

GENDER = (  
    ('F', 'Female'),
    ('M', 'Male'),
)

SUBURBS = (
    ('SUN', 'Sunshine'),
    ('DP', 'Deer Park'),
    ('SA', 'St. Albans'),
    ('SYD', 'Sydenham'),
    ('ALB', 'Albion'),
)

SKILLS = (
    ('ENG', 'English'),
    ('MATH', 'Math'),
    ('GUIT', 'Guitar'),
    ('FOOT', 'Football'),
    ('SCI', 'Science'),
    ('BUS', 'Business'),
)

LANGUAGES = (
    ('ENG', 'English'),
    ('VIET', 'Vietnamese'),
    ('CHI', 'Chinese'),
)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/document/{1}'.format(instance.user.id, filename)

def user_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/image/{1}'.format(instance.user.id, filename)

class TagModel(tagulous.models.TagModel):
    class TagMeta:
        pass

# class SkillCategory(models.Model):
    # category_name = models.CharField(max_length=50)

    # def __str__(self):
        # return self.category_name

class NewSkill(models.Model):
    skill_name = models.CharField(max_length=50, help_text='The skill name', blank=True)
    # category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, default = 1, blank=True)

    def __str__(self):
        return self.skill_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    # document = models.FileField(upload_to='documents/', blank=True)
    document = models.FileField(upload_to=user_directory_path, blank=True)
    avatar = models.ImageField(upload_to=user_image_directory_path, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    suburb = models.CharField(max_length=3, choices=SUBURBS, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    # skill = models.CharField(max_length=100, choices=SKILLS, blank=True)
    # skill = MultiSelectField(choices=SKILLS, max_choices=3, blank=True) # this will create MultipleChoice field
    skill = models.ManyToManyField(NewSkill, blank=True, related_name='profiles')
    # skill = select2.fields.ManyToManyField(NewSkill) #this is for generating select2 field in admin site
    language = MultiSelectField(choices=LANGUAGES, max_choices=3)
    # skillcategory = models.ManyToManyField(SkillCategory)
    # skillcategory = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, default = 1, blank=True)

    def __str__(self):
        return self.user.username