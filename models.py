from django.db import models

class MaintenanceRequest(models.Model):
    STAGES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("repaired", "Repaired"),
        ("scrap", "Scrap"),
    ]

    TYPES = [
        ("corrective", "Corrective"),
        ("preventive", "Preventive"),
    ]

    subject = models.CharField(max_length=200)
    equipment = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    employee = models.CharField(max_length=100)
    technician = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=20, choices=STAGES, default="new")
    maintenance_type = models.CharField(max_length=20, choices=TYPES)
    request_date = models.DateField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    duration_hours = models.FloatField(default=0)
    priority = models.IntegerField(default=1)
    company = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.subject
