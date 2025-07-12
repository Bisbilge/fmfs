from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError
from products.models import Product

class CustomUser(AbstractUser):
    money = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    max_carry_weight = models.FloatField(
        default=10.0
    )

    def __str__(self):
        return self.username

    @property
    def current_carry_weight(self):
        return sum(
            item.quantity * item.product.weight
            for item in self.inventory_items.select_related('product').all()
        )
class ProductionExpertise(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expertises'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='expert_users'
    )
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} – {self.product.name} (Lv. {self.level}, XP: {self.xp})"

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.required_xp_for_next_level():
            self.xp -= self.required_xp_for_next_level()
            self.level += 1
        self.save()

    def required_xp_for_next_level(self):
        # Seviye³ bazlı artış yerine seviye² bazlı bırakılabilir, örnek olarak:
        return 100 * (self.level ** 2)

    def production_speed_multiplier(self):
        # Seviye arttıkça %10 hız artışı örneği
        return 1.0 / (1 + (self.level - 1) * 0.1)
    
class Inventory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='held_by_users'
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} has {self.quantity}×{self.product.name}"

    def clean(self):
        # Eski miktarı _old_qty’de saklıyoruz
        total_after = (
            self.user.current_carry_weight
            - (getattr(self, '_old_qty', 0) * self.product.weight)
            + (self.quantity * self.product.weight)
        )
        if total_after > self.user.max_carry_weight:
            raise ValidationError(
                f"Taşıma kapasitenizi aşıyorsunuz! "
                f"({total_after:.2f}kg / {self.user.max_carry_weight}kg)"
            )

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Inventory.objects.get(pk=self.pk)
            self._old_qty = orig.quantity
        else:
            self._old_qty = 0
        self.full_clean()
        super().save(*args, **kwargs)

    def add(self, amount: int):
        self.quantity = (self.quantity or 0) + amount
        self.save()

    def remove(self, amount: int):
        if (self.quantity or 0) < amount:
            raise ValidationError("Yeterli stok yok")
        self.quantity = self.quantity - amount
        self.save()
