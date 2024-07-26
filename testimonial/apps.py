from django.apps import AppConfig

class TestimonialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testimonial'

    def ready(self):
        import testimonial.signals  # Ensure this line is present to load signals
