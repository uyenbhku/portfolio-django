from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Profile(models.Model):
    """Central profile for the portfolio owner."""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100)

    bio_short = models.TextField(help_text="Brief introduction for homepage")
    bio_full = models.TextField(help_text="Detailed about me section")

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name


class Technology(models.Model):
    """Skills, languages, frameworks, and tools in one flexible model."""

    CATEGORY_CHOICES = [
        ('language', 'Programming Language'),
        ('framework', 'Framework'),
        ('tool', 'Tool'),
        ('database', 'Database'),
        ('other', 'Other'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    LEVEL_ORDER = {
        'expert': 4,
        'advanced': 3,
        'intermediate': 2,
        'beginner': 1,
    }

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.FileField(upload_to='technology_icons/', blank=True)
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner',
        help_text="Your proficiency level in this technology",
    )
    is_featured = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    @property
    def level_score(self):
        return self.LEVEL_ORDER.get(self.level, 0)


class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('live', 'Live'),
    ]

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='projects'
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(
        max_length=200,
        help_text="A brief summary for cards/previews",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    technologies = models.ManyToManyField(Technology, related_name='projects')
    repository_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    document_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_featured = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    priority = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'project'
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    @property
    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class Experience(models.Model):
    """Shared fields for education and work history."""

    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    highlights = models.JSONField(
        default=list,
        help_text="List of key achievements/responsibilities",
    )

    class Meta:
        abstract = True
        ordering = ['-start_date']

    @property
    def date_range(self):
        start = self.start_date.strftime('%b %Y')
        end = 'Present' if self.is_current or not self.end_date else self.end_date.strftime('%b %Y')
        return f'{start} – {end}'


class Education(Experience):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='education'
    )
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.degree} — {self.organization}'


class WorkExperience(Experience):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='work_experience'
    )
    technologies_used = models.ManyToManyField(
        Technology, related_name='work_experiences', blank=True
    )

    def __str__(self):
        return f'{self.title} @ {self.organization}'


class BlogPost(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='blog_posts'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(help_text="Brief preview of the post")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('published', 'Published')],
        default='draft',
    )

    technologies = models.ManyToManyField(
        Technology, related_name='blog_posts', blank=True
    )
    featured_image = models.ImageField(upload_to='blog/%Y/%m/', blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'post'
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject or "No subject"}'
