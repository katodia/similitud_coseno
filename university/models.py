from django.db import models


class University(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Universities'


class Area(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    total_credits = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.area.name})"


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    credits = models.IntegerField(default=0)
    is_optional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Related(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    related = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='related')
    value = models.DecimalField(max_digits=10, decimal_places=8, default=0.0)

    def __str__(self):
        return f"{self.name}"

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
