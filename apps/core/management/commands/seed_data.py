"""Seed the database with the admin account and starter demo content.

Usage:  python manage.py seed_data
Reads ADMIN_USERNAME / ADMIN_PASSWORD / ADMIN_EMAIL from the environment (.env).
"""
import os
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.core.models import (
    Achievement, Certificate, Education, Experience, FAQ, Profile, Project,
    Resume, SiteSettings, Skill, SocialLink,
)


class Command(BaseCommand):
    help = "Create the admin user and populate starter content."

    def handle(self, *args, **options):
        self.create_admin()
        self.create_settings()
        self.create_profile()
        self.create_education()
        self.create_experience()
        self.create_skills()
        self.create_projects()
        self.create_certificates()
        self.create_achievements()
        self.create_social_links()
        self.create_faqs()
        self.stdout.write(self.style.SUCCESS("Seed data complete."))

    def create_admin(self):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        if not password:
            raise CommandError(
                "ADMIN_PASSWORD is not set. Add it to your .env file and retry."
            )
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f"Created admin user '{username}'.")
        else:
            self.stdout.write(f"Admin user '{username}' already exists.")

    @staticmethod
    def _get_or_create(model, defaults, **lookup):
        obj, created = model.objects.get_or_create(defaults=defaults, **lookup)
        return obj, created

    def create_settings(self):
        obj, created = self._get_or_create(
            SiteSettings, pk=1,
            defaults={
                "site_title": "Anuj Biswal | AI & ML Engineer",
                "tagline": "AI Engineer & Full-Stack Developer",
                "meta_description": "Portfolio of Anuj Biswal - AI/ML Engineer, Full-Stack Developer and tech enthusiast.",
                "primary_color": "#6c5ce7",
                "accent_color": "#00d4ff",
                "footer_text": "© 2026 Anuj Biswal. Crafted with passion & code.",
            },
        )
        self.stdout.write("Site settings: " + ("created" if created else "exists"))

    def create_profile(self):
        obj, created = self._get_or_create(
            Profile, pk=1,
            defaults={
                "name": "Anuj Biswal",
                "title": "AI & Machine Learning Engineer",
                "tagline": "Building intelligent systems that solve real-world problems.",
                "bio": (
                    "Hi, I am Anuj Biswal - an AI & Machine Learning engineer with a passion for "
                    "building intelligent products. I design, train and ship ML models and "
                    "full-stack applications that are fast, secure and delightful to use."
                ),
                "career_objective": (
                    "To leverage my expertise in AI, machine learning and software engineering "
                    "to build products that create measurable impact, while continuously "
                    "learning and mentoring others."
                ),
                "journey": (
                    "My journey started with curiosity about how machines learn. From building "
                    "small scripts to training deep neural networks, every project taught me "
                    "something new about engineering, design and problem solving."
                ),
                "mission": "Democratize AI by building tools that are accessible, ethical and practical.",
                "vision": "A world where every engineer can leverage AI to amplify human creativity.",
                "email": "anuj.biswal@example.com",
                "phone": "+91 00000 00000",
                "location": "Odisha, India",
                "typing_roles": ["AI Engineer", "ML Enthusiast", "Full-Stack Developer", "Problem Solver"],
                "interests": ["Artificial Intelligence", "Open Source", "Chess", "Cricket", "Reading"],
            },
        )
        self.stdout.write("Profile: " + ("created" if created else "exists"))

    def create_education(self):
        rows = [
            {"institution": "B.Tech in Computer Science & Engineering", "degree": "Bachelor of Technology",
             "field_of_study": "CSE with AI/ML specialization", "start_year": 2023, "end_year": None,
             "description": "Focusing on machine learning, data structures, and full-stack development."},
            {"institution": "Higher Secondary School", "degree": "Class XII (Science)",
             "field_of_study": "PCM + Computer Science", "start_year": 2020, "end_year": 2022,
             "description": "Completed senior secondary education with a focus on mathematics and computer science."},
        ]
        for i, row in enumerate(rows):
            obj, created = self._get_or_create(Education, institution=row["institution"], degree=row["degree"], defaults={**row, "order": i})
            self.stdout.write(f"  Education: {obj.institution} (created)" if created else "")

    def create_experience(self):
        rows = [
            {"role": "AI/ML Intern", "company": "TechNova Labs", "location": "Remote",
             "start_date": date(2025, 6, 1), "end_date": None, "current": True,
             "description": "Building computer vision pipelines and fine-tuning transformer models for production use cases."},
            {"role": "Freelance Web Developer", "company": "Self-employed", "location": "Remote",
             "start_date": date(2024, 1, 1), "end_date": date(2025, 5, 31), "current": False,
             "description": "Designed and deployed responsive web apps for small businesses using Django and Bootstrap."},
        ]
        for i, row in enumerate(rows):
            obj, created = self._get_or_create(Experience, role=row["role"], company=row["company"], defaults={**row, "order": i})
            self.stdout.write(f"  Experience: {obj.role} (created)" if created else "")

    def create_skills(self):
        rows = [
            ("Python", "programming", "bi-filetype-py", 92),
            ("C / C++", "programming", "bi-cpu", 85),
            ("Java", "programming", "bi-cup-hot", 70),
            ("JavaScript (ES6+)", "frontend", "bi-filetype-js", 84),
            ("HTML5 & CSS3", "frontend", "bi-filetype-html", 88),
            ("Bootstrap 5", "frontend", "bi-bootstrap", 86),
            ("React", "frontend", "bi-react", 74),
            ("Django", "backend", "bi-layers", 87),
            ("REST APIs", "backend", "bi-hdd-network", 82),
            ("MySQL", "database", "bi-database", 80),
            ("SQLite / PostgreSQL", "database", "bi-database-gear", 78),
            ("Machine Learning", "ml", "bi-cpu-fill", 85),
            ("Deep Learning", "ml", "bi-diagram-3", 76),
            ("TensorFlow / Keras", "ai", "bi-stars", 78),
            ("Computer Vision", "ai", "bi-eye-fill", 80),
            ("Pandas & NumPy", "ml", "bi-table", 88),
            ("Git & GitHub", "tools", "bi-git", 90),
            ("Docker", "cloud", "bi-box-seam", 72),
            ("AWS (Basics)", "cloud", "bi-cloud", 68),
            ("Linux", "tools", "bi-terminal", 75),
            ("Problem Solving", "soft", "bi-lightbulb", 90),
            ("Team Leadership", "soft", "bi-people-fill", 82),
        ]
        for i, (name, category, icon, level) in enumerate(rows):
            obj, created = self._get_or_create(Skill, name=name, defaults={
                "category": category, "icon": icon, "level": level, "order": i})
            if created:
                self.stdout.write(f"  Skill: {name} (created)")

    def create_projects(self):
        rows = [
            {"title": "Weapon Detection System",
             "description": "Real-time weapon detection using YOLO and OpenCV with a FastAPI backend, alert pipeline and analytics dashboard.",
             "category": "ai", "status": "completed", "featured": True,
             "technologies": ["Python", "YOLO", "OpenCV", "FastAPI", "Docker"],
             "github_url": "https://github.com/anujbiswal/weapon-detection",
             "live_url": "https://example.com/weapon-detection",
             "start_date": date(2025, 3, 1), "order": 0},
            {"title": "AI Traffic Prediction",
             "description": "Traffic flow forecasting engine using time-series ML models served through a Django web app with live visualizations.",
             "category": "ai", "status": "ongoing", "featured": True,
             "technologies": ["Python", "scikit-learn", "Django", "PostgreSQL"],
             "github_url": "https://github.com/anujbiswal/traffic-prediction",
             "live_url": "",
             "start_date": date(2025, 6, 1), "order": 1},
            {"title": "JARVIS-X Assistant",
             "description": "A lightweight desktop AI assistant with RAG-powered memory, speech recognition and local LLM integration.",
             "category": "ai", "status": "completed", "featured": True,
             "technologies": ["Python", "RAG", "LangChain", "Tkinter"],
             "github_url": "https://github.com/anujbiswal/jarvis-x",
             "live_url": "",
             "start_date": date(2024, 11, 1), "order": 2},
            {"title": "Student Management System",
             "description": "Full-stack CRUD application for managing student records with role-based access and report generation.",
             "category": "web", "status": "completed", "featured": False,
             "technologies": ["Python", "Django", "Bootstrap 5", "SQLite"],
             "github_url": "https://github.com/anujbiswal/student-management",
             "live_url": "",
             "start_date": date(2024, 8, 1), "order": 3},
        ]
        for row in rows:
            obj, created = self._get_or_create(Project, title=row["title"], defaults=row)
            if created:
                self.stdout.write(f"  Project: {row['title']} (created)")

    def create_certificates(self):
        rows = [
            ("Machine Learning Specialization", "DeepLearning.AI", "ai", "2025-04-15", 0),
            ("Python for Everybody", "Coursera / University of Michigan", "programming", "2024-06-10", 1),
            ("Django Web Framework", "Coding Ninjas", "web", "2024-09-20", 2),
            ("AWS Cloud Practitioner (In Progress)", "Amazon Web Services", "cloud", None, 3),
        ]
        for title, issuer, category, issued, order in rows:
            obj, created = self._get_or_create(Certificate, title=title, defaults={
                "issuer": issuer, "category": category, "order": order,
                "issued_date": date.fromisoformat(issued) if issued else None,
                "credential_id": f"CRED-{order:04d}",
                "credential_url": "https://example.com/verify",
            })
            if created:
                self.stdout.write(f"  Certificate: {title} (created)")

    def create_achievements(self):
        rows = [
            ("Winner - Campus AI Hackathon 2025", "hackathon", "2025-02-14", 0),
            ("Completed 30-day ML Challenge", "event", "2024-12-20", 1),
            ("Speaker at College Tech Workshop", "workshop", "2024-10-05", 2),
            ("Top 5% - DSA Coding Contest", "college", "2024-08-30", 3),
        ]
        for title, category, when, order in rows:
            obj, created = self._get_or_create(Achievement, title=title, defaults={
                "category": category, "date": date.fromisoformat(when), "order": order,
                "description": "Milestone achieved through consistent effort, learning and teamwork.",
            })
            if created:
                self.stdout.write(f"  Achievement: {title} (created)")

    def create_social_links(self):
        rows = [
            ("github", "https://github.com/anujbiswal", 0),
            ("linkedin", "https://linkedin.com/in/anujbiswal", 1),
            ("instagram", "https://instagram.com/anujbiswal", 2),
            ("leetcode", "https://leetcode.com/anujbiswal", 3),
            ("codechef", "https://codechef.com/users/anujbiswal", 4),
            ("hackerrank", "https://hackerrank.com/anujbiswal", 5),
            ("twitter", "https://x.com/anujbiswal", 6),
            ("youtube", "https://youtube.com/@anujbiswal", 7),
            ("medium", "https://medium.com/@anujbiswal", 8),
        ]
        for platform, url, order in rows:
            obj, created = self._get_or_create(SocialLink, platform=platform, defaults={"url": url, "order": order})
            if created:
                self.stdout.write(f"  Social: {platform} (created)")

    def create_faqs(self):
        rows = [
            ("Who is Anuj?",
             "Anuj Biswal is an AI & Machine Learning engineer who loves building intelligent products - from computer vision systems to full-stack web apps.",
             "who, about, anuj, bio, profile", 0),
            ("What technologies does Anuj know?",
             "Anuj works with Python, Django, JavaScript, Machine Learning, Deep Learning, TensorFlow, OpenCV, SQL databases, Docker and Git, among others.",
             "technologies, tech, stack, skills, tools, languages", 1),
            ("How can I contact Anuj?",
             "Use the contact form on this site, or reach out via email, LinkedIn or GitHub - all links are available on the Contact page and in the footer.",
             "contact, email, reach, hire, message", 2),
            ("Where is Anuj studying?",
             "Anuj is pursuing a B.Tech in Computer Science & Engineering with a specialization in AI/ML.",
             "education, study, college, university, degree", 3),
            ("Show certificates",
             "Head over to the Certificates page to see Anuj's certifications and credentials. You can filter by category and download PDFs.",
             "certificates, certifications, courses, credentials", 4),
            ("Show projects",
             "Check out the Projects page for the full portfolio - you can search, filter by category/status, and open live demos or GitHub repositories.",
             "projects, work, portfolio, github, demos", 5),
            ("What are Anuj's skills?",
             "Anuj's skills span frontend, backend, AI/ML, cloud, databases and soft skills - see the Skills page for animated progress charts.",
             "skills, abilities, expertise, strengths", 6),
            ("Does Anuj have work experience?",
             "Yes - Anuj has experience as an AI/ML intern and freelance web developer. See the Experience and Timeline pages for details.",
             "experience, work, jobs, internship, timeline", 7),
        ]
        for question, answer, keywords, order in rows:
            obj, created = self._get_or_create(FAQ, question=question, defaults={
                "answer": answer, "keywords": keywords, "order": order})
            if created:
                self.stdout.write(f"  FAQ: {question[:40]} (created)")
