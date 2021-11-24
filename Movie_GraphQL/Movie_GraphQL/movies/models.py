from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return self.title
