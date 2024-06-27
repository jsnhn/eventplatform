from django.db import models

# Create your models here.

GROUPS = (
    ('M', 'Music'),
    ('F', 'Food & Drink'),
    ('H', 'Hobbies'),
    ('T', 'Theater'),
    ('D', 'Dating'),
)

class Event(models.Model):
    name = models.CharField(max_length=100),
    short_summary = models.CharField(max_length=100),
    category = models.CharField(
        max_length=1,
        choices=GROUPS,
        default=GROUPS[0][0]
    )
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    about = models.CharField(max_length=200)
    age_restriction = models.IntegerField()

    def __str__ (self):
        return self.name