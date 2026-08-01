"""Database models - normalized, single source of truth for the whole site."""
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base adding created/updated timestamps to every model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SingletonManager(models.Manager):
    """Manager that returns the single instance of a singleton model."""

    def get_queryset(self):
        return super().get_queryset().filter(pk=1)


class Profile(TimeStampedModel):
    """Personal information shown across the viewer site."""

    objects = SingletonManager()

    name = models.CharField(max_length=120, default="Anuj Biswal")
    title = models.CharField(max_length=200, default="AI & Machine Learning Engineer")
    tagline = models.TextField(
        blank=True, default="Building intelligent systems that solve real-world problems."
    )
    bio = models.TextField(blank=True, help_text="Full biography for the About page.")
    career_objective = models.TextField(blank=True)
    journey = models.TextField(blank=True, help_text="Your story / how you started - About page.")
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    cover_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    typing_roles = models.JSONField(default=list, blank=True, help_text="Roles animated in the hero, e.g. AI Engineer, Full-Stack Developer.")
    interests = models.JSONField(default=list, blank=True, help_text="List of interests (chips on About page).")

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.name

    @classmethod
    def load(cls):
        """Fetch the singleton profile, creating it with defaults on first use."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)


class SiteSettings(TimeStampedModel):
    """Global site configuration: title, SEO, theme colors, logo, analytics."""

    objects = SingletonManager()

    site_title = models.CharField(max_length=200, default="Anuj Biswal | AI & ML Engineer")
    tagline = models.CharField(max_length=200, blank=True, default="AI Engineer & Full-Stack Developer")
    meta_description = models.TextField(blank=True, default="Portfolio of Anuj Biswal - AI/ML Engineer, Full-Stack Developer.")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    primary_color = models.CharField(max_length=9, default="#6c5ce7", help_text="Hex color, e.g. #6c5ce7")
    accent_color = models.CharField(max_length=9, default="#00d4ff", help_text="Hex color, e.g. #00d4ff")
    analytics_code = models.TextField(blank=True, help_text="Optional analytics snippet.")
    map_embed_url = models.URLField(blank=True, help_text="Google Maps embed URL for the contact page.")
    footer_text = models.CharField(max_length=300, blank=True, default="(c) 2026 Anuj Biswal. Crafted with passion & code.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.site_title

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class Education(TimeStampedModel):
    """Education record used by About and Timeline pages."""

    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True, help_text="Leave empty if still studying.")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "-start_year")
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    def year_range(self):
        end = str(self.end_year) if self.end_year else "Present"
        return f"{self.start_year} - {end}"


class Experience(TimeStampedModel):
    """Work experience shown on Experience and Timeline pages."""

    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="Leave empty for the current role.")
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "-start_date")

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def date_range(self):
        end = self.end_date.strftime("%b %Y") if self.end_date else "Present"
        return f"{self.start_date.strftime('%b %Y')} - {end}"


SKILL_CATEGORIES = (
    ("frontend", "Frontend"),
    ("backend", "Backend"),
    ("ai", "AI"),
    ("ml", "Machine Learning"),
    ("cloud", "Cloud"),
    ("programming", "Programming"),
    ("database", "Database"),
    ("tools", "Tools"),
    ("soft", "Soft Skills"),
)


class Skill(TimeStampedModel):
    """A skill with a proficiency level and a Bootstrap Icons icon."""

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, default="programming")
    icon = models.CharField(max_length=60, blank=True, default="bi-code-slash", help_text="Bootstrap Icons class, e.g. bi-python")
    level = models.PositiveIntegerField(default=70, help_text="0 - 100")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("category", "order", "name")

    def __str__(self):
        return self.name


PROJECT_STATUS = (("completed", "Completed"), ("ongoing", "Ongoing"), ("planned", "Planned"))
PROJECT_CATEGORIES = (
    ("ai", "AI / ML"),
    ("web", "Web Development"),
    ("app", "Applications"),
    ("research", "Research"),
    ("other", "Other"),
)


class Project(TimeStampedModel):
    """A portfolio project with media, links, tags and visibility flags."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=PROJECT_CATEGORIES, default="ai")
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default="completed")
    featured = models.BooleanField(default=False, help_text="Show on the home page.")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="Optional video (YouTube / MP4).")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True, help_text="Live demo link.")
    technologies = models.JSONField(default=list, blank=True, help_text="e.g. [Python, TensorFlow, Django]")
    start_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-featured", "order", "-created_at")

    def __str__(self):
        return self.title


CERT_CATEGORIES = (
    ("ai", "AI / ML"),
    ("web", "Web Development"),
    ("cloud", "Cloud"),
    ("programming", "Programming"),
    ("soft", "Soft Skills"),
    ("other", "Other"),
)


class Certificate(TimeStampedModel):
    """A certificate with optional image, PDF download and verification link."""

    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CERT_CATEGORIES, default="ai")
    issued_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="certificates/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="certificates/", blank=True, null=True, help_text="Optional PDF for download.")
    credential_id = models.CharField(max_length=120, blank=True)
    credential_url = models.URLField(blank=True, help_text="Verification link.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "-issued_date")

    def __str__(self):
        return self.title


ACHIEVEMENT_CATEGORIES = (
    ("hackathon", "Hackathon"),
    ("workshop", "Workshop"),
    ("college", "College"),
    ("event", "Event"),
    ("other", "Other"),
)


class Achievement(TimeStampedModel):
    """An achievement / award / milestone."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=ACHIEVEMENT_CATEGORIES, default="other")
    date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="achievements/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "-date")

    def __str__(self):
        return self.title


GALLERY_CATEGORIES = (
    ("achievements", "Achievements"),
    ("hackathon", "Hackathons"),
    ("workshop", "Workshops"),
    ("college", "College"),
    ("event", "Events"),
    ("other", "Other"),
)


class GalleryImage(TimeStampedModel):
    """An image shown in the public gallery."""

    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="gallery/")
    category = models.CharField(max_length=20, choices=GALLERY_CATEGORIES, default="other")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "-created_at")
        verbose_name = "Gallery image"
        verbose_name_plural = "Gallery images"

    def __str__(self):
        return self.title or f"Gallery image #{self.pk}"


class Resume(TimeStampedModel):
    """A resume PDF. The viewer always sees the latest active version."""

    label = models.CharField(max_length=120, blank=True, default="Latest Resume")
    file = models.FileField(upload_to="resumes/", help_text="PDF file.")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.label

    @classmethod
    def latest(cls):
        return cls.objects.filter(is_active=True).order_by("-created_at", "-id").first()


SOCIAL_PLATFORMS = (
    ("github", "GitHub", "bi-github"),
    ("linkedin", "LinkedIn", "bi-linkedin"),
    ("instagram", "Instagram", "bi-instagram"),
    ("slack", "Slack", "bi-slack"),
    ("twitter", "Twitter / X", "bi-twitter-x"),
    ("leetcode", "LeetCode", "bi-code-square"),
    ("codechef", "CodeChef", "bi-egg-fried"),
    ("hackerrank", "HackerRank", "bi-trophy"),
    ("youtube", "YouTube", "bi-youtube"),
    ("medium", "Medium", "bi-medium"),
    ("portfolio", "Portfolio", "bi-globe2"),
)


class SocialLink(TimeStampedModel):
    """A social/community profile link editable from the admin panel."""

    platform = models.CharField(max_length=20, choices=[(p[0], p[1]) for p in SOCIAL_PLATFORMS])
    url = models.URLField(max_length=400)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "platform")

    def __str__(self):
        return self.get_platform_display()

    @property
    def icon(self):
        for code, _label, icon in SOCIAL_PLATFORMS:
            if code == self.platform:
                return icon
        return "bi-link-45deg"


class ContactMessage(TimeStampedModel):
    """A message submitted through the public contact form."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}: {self.subject or self.message[:40]}"


class FAQ(TimeStampedModel):
    """Predefined Q&A used by the floating AI assistant (no LLM involved)."""

    question = models.CharField(max_length=300)
    answer = models.TextField()
    keywords = models.CharField(max_length=300, blank=True, help_text="Extra matching words, comma separated.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Visitor(models.Model):
    """Lightweight visit log powering the dashboard visitor stats."""

    session_key = models.CharField(max_length=64, db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=500, default="/")
    user_agent = models.CharField(max_length=500, blank=True)
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-last_seen",)

    def __str__(self):
        return f"{self.session_key} - {self.path}"
