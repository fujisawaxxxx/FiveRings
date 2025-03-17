from django.db import models

# Create your models here.

class Project(models.Model):
    project_name = models.CharField(max_length=200, verbose_name="プロジェクト名")

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "プロジェクト"
        verbose_name_plural = "プロジェクト"
