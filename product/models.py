from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'menu'

class Category(models.Model):
    menu        = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name        = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'categories'

class Product(models.Model):
    category       = models.ForeignKey('Category', on_delete=models.CASCADE)
    name           = models.CharField(max_length=45)
    sub_name       = models.CharField(max_length=45)
    description    = models.CharField(max_length=3000)
    nutrition_url  = models.URLField(max_length=2000)
    is_new         = models.BooleanField(default=False)
    vegan_level    = models.ForeignKey('VeganLevel', on_delete=models.CASCADE)
    is_default     = models.BooleanField(default=False)
    gender_code    = models.ForeignKey('GenderCode', on_delete=models.CASCADE)
    age_level      = models.ForeignKey('AgeLevel', on_delete=models.CASCADE)
    activity_level = models.ForeignKey('ActivityLevel', on_delete=models.CASCADE)
    care_smoker    = models.BooleanField(default=False)
    care_drinker   = models.BooleanField(default=False)
    care_obesity   = models.BooleanField(default=False)
    disease        = models.ManyToManyField('Disease', through='ProductDisease')
    allergy        = models.ManyToManyField('Allergy', through='ProductAllergy')
    dietary_habit  = models.ManyToManyField('DietaryHabit', through='ProductDietaryHabit')
    goal           = models.ManyToManyField('Goal', through='ProductGoal')

    class Meta:
        db_table = 'products'

class Image(models.Model):
    product        = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url      = models.URLField(max_length=2000)
    is_main        = models.BooleanField(default=False)

    class Meta:
        db_table='images'
    
class ProductStock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.CharField(max_length=20, null=True)
    price   = models.DecimalField(max_digits=10, decimal_places=2)
    stock   = models.IntegerField()

    class Meta:
        db_table = 'product_stocks'

class RelatedProduct(models.Model):
    standard_product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='related_product')
    related_product  = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='standard_product')

    class Meta:
        db_table = 'related_products'

class Disease(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'diseases'

class ProductDisease(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    disease = models.ForeignKey('Disease', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_diseases'

class Allergy(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table='allergies'

class ProductAllergy(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    allergy = models.ForeignKey('Allergy', on_delete=models.CASCADE)

    class Meta:
        db_table='product_allergies'

class Goal(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'goals'

class ProductGoal(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    goal    = models.ForeignKey('Goal', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_goals'

class DietaryHabit(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'dietary_habits'

class ProductDietaryHabit(models.Model):
    product       = models.ForeignKey('Product', on_delete=models.CASCADE)
    dietary_habit = models.ForeignKey('DietaryHabit', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_dietary_habits'

class VeganLevel(models.Model):
    id   = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'vegan_levels'

class ActivityLevel(models.Model):
    id   = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'activity_levels'

class GenderCode(models.Model):
    id   = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'gender_codes'

class AgeLevel(models.Model):
    id   = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'age_levels'

