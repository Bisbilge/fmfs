from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    weight = models.FloatField()
    is_edible = models.BooleanField(default=False)
    energy = models.IntegerField(blank=True, null=True)
    decay_time = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='recipe',
        help_text='Bu tarifin çıktısı olan ürün'
    )
    output_quantity = models.PositiveIntegerField(
        default=1,
        help_text='Bu tariften kaç birim ürün elde edilir'
    )
    craft_time = models.PositiveIntegerField(
        default=0,
        help_text='Üretim süresi (saniye cinsinden)'
    )

    def __str__(self):
        return f"Recipe for {self.product.name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='used_in'
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity}×{self.ingredient.name} for {self.recipe.product.name}"
