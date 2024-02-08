from django.db import models

# Create your models here.
class Project(models.Model):
    select_status = [
        ('Ongoing', 'Ongoing'),
        ('Done', 'Done'),
        ('Canceled', 'Cancelled'),
        ('IsLived', 'IsLived'),
    ]

    title = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    course_name = models.TextField()
    document_link = models.TextField()
    code = models.TextField()
    thumbnail = models.ImageField(upload_to='images/')
    author = models.TextField()
    tag = models.TextField()
    status = models.CharField(max_length=20, choices=select_status)
    is_hidden = models.BooleanField(default=False)
    live_url = models.TextField(null=True)


    def get_thumbnail_url(self):
        return self.thumbnail.url



class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def get_client_message(self):
        return f"""
            Client: {self.name} \t Email: {self.email}
            Message: 
            {self.message}
        """

class AbstractSkillOverview(models.Model):
    name = models.CharField(max_length=30)
    is_hidden = models.BooleanField(default=False)
    owner = models.ForeignKey("MyInfo", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MySkill(AbstractSkillOverview):
    pass


class MyTool(AbstractSkillOverview):
    pass


class MyLanguage(AbstractSkillOverview):
    pass


class MyTitle(AbstractSkillOverview):
    pass


class MyInfo(models.Model):
    home_description = models.TextField()
    portfolio_description = models.TextField()
    owner = models.CharField(max_length=40, default='Uyen Kim', primary_key=True)
    resume = models.FileField(upload_to='resumes/', null=True)
    personal_image = models.ImageField(upload_to='myself/', null=True)