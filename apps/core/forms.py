"""ModelForms for the admin panel and the public contact form."""
import json

from django import forms

from .models import (
    Achievement, Certificate, ContactMessage, Education, Experience, FAQ,
    GalleryImage, Profile, Project, Resume, SiteSettings, Skill, SocialLink,
)


def split_list(value):
    """Convert text (comma / newline / JSON array) into a list of strings."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed if str(x).strip()]
    except (ValueError, TypeError):
        pass
    return [part.strip() for part in text.replace("\n", ",").split(",") if part.strip()]


class BaseModelForm(forms.ModelForm):
    """Applies consistent Bootstrap classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.URLInput, forms.EmailInput,
                                  forms.NumberInput, forms.DateInput)):
                widget.attrs.setdefault("class", "form-control")
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "form-control")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("class", "form-control form-file")


class ProfileForm(BaseModelForm):
    typing_roles = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control",
                                     "placeholder": "AI Engineer, Full-Stack Developer"}),
    )
    interests = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control",
                                     "placeholder": "AI, Chess, Cricket, Reading"}),
    )

    class Meta:
        model = Profile
        fields = ["name", "title", "tagline", "bio", "career_objective", "journey",
                  "mission", "vision", "email", "phone", "location", "date_of_birth",
                  "profile_image", "cover_image", "typing_roles", "interests"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}

    def clean_typing_roles(self):
        return split_list(self.cleaned_data.get("typing_roles"))

    def clean_interests(self):
        return split_list(self.cleaned_data.get("interests"))


class SiteSettingsForm(BaseModelForm):
    class Meta:
        model = SiteSettings
        fields = ["site_title", "tagline", "meta_description", "logo", "favicon",
                  "primary_color", "accent_color", "analytics_code", "map_embed_url",
                  "footer_text"]
        widgets = {"primary_color": forms.TextInput(attrs={"type": "color"}),
                   "accent_color": forms.TextInput(attrs={"type": "color"})}


class EducationForm(BaseModelForm):
    class Meta:
        model = Education
        fields = ["institution", "degree", "field_of_study", "start_year", "end_year",
                  "description", "order"]


class ExperienceForm(BaseModelForm):
    class Meta:
        model = Experience
        fields = ["role", "company", "location", "start_date", "end_date", "current",
                  "description", "order"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"}),
                   "end_date": forms.DateInput(attrs={"type": "date"})}


class SkillForm(BaseModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "icon", "level", "order"]


class ProjectForm(BaseModelForm):
    technologies = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control",
                                     "placeholder": "Python, TensorFlow, Django"}),
    )

    class Meta:
        model = Project
        fields = ["title", "description", "category", "status", "featured", "image",
                  "video_url", "github_url", "live_url", "technologies", "start_date",
                  "order"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"})}

    def clean_technologies(self):
        return split_list(self.cleaned_data.get("technologies"))


class CertificateForm(BaseModelForm):
    class Meta:
        model = Certificate
        fields = ["title", "issuer", "category", "issued_date", "image", "pdf_file",
                  "credential_id", "credential_url", "order"]
        widgets = {"issued_date": forms.DateInput(attrs={"type": "date"})}


class AchievementForm(BaseModelForm):
    class Meta:
        model = Achievement
        fields = ["title", "description", "category", "date", "image", "order"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class GalleryImageForm(BaseModelForm):
    class Meta:
        model = GalleryImage
        fields = ["title", "image", "category", "order"]


class ResumeForm(BaseModelForm):
    class Meta:
        model = Resume
        fields = ["label", "file", "is_active"]


class SocialLinkForm(BaseModelForm):
    class Meta:
        model = SocialLink
        fields = ["platform", "url", "order"]


class FAQForm(BaseModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "keywords", "order"]


class ContactMessageForm(BaseModelForm):
    """Public contact form with a hidden honeypot anti-spam field."""

    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Your message..."}),
        }
