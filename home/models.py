from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    course_name = models.TextField()
    document_link = models.TextField()
    code = models.TextField()
    thumbnail = models.ImageField(upload_to='images/')
    author = models.TextField()
    tag = models.TextField()


    def get_thumbnail_url(self):
        return self.thumbnail.url



class ContactInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()


    def get_client_message(self):
        return f"""
            Client: {self.name} \t Email: {self.email}
            Message: 
            {self.message}
        """