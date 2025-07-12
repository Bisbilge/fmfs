from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 

class CustomUser(AbstractUser):
    money = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)


    def __str__(self):
        return self.username

class ProductionExpertise(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expertises')
    product_name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'product_name')

    def __str__(self):
        return f"{self.user.username} - {self.product_name} (Lv. {self.level}, XP: {self.xp})"

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.required_xp_for_next_level():
            self.xp -= self.required_xp_for_next_level()
            self.level += 1
        self.save()

    def required_xp_for_next_level(self):
        return 100 * (self.level ** 2)

    def production_speed_multiplier(self):
        return 1.0 / (1 + (self.level - 1) * 0.1)  
