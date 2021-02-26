from django.db import models

class QuizResult(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recommendations'