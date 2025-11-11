from django.db import models
from django.contrib.auth.models import User

class AnalysisReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=50)
    probability = models.FloatField()
    sources = models.JSONField(default=list, blank=True)
    signs_of_falsification = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "file_name": self.file_name,
            "label": self.label,
            "probability": round(self.probability, 4),
            "sources": self.sources,
            "signs_of_falsification": self.signs_of_falsification,
            "created_at": self.created_at.isoformat()
        }
