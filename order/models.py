from django.db      import models

class Promotion(models.Model):
    code           = models.CharField(max_length=30)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'promotions'

class Order(models.Model):
    user            = models.ForeignKey('user.User', on_delete=models.SET_DEFAULT, default=1)
    order_number    = models.CharField(max_length=300)
    order_status    = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True)
    shipment_status = models.ForeignKey('ShipmentStatus', on_delete=models.SET_NULL, null=True)
    sub_total_cost  = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost   = models.DecimalField(max_digits=10, decimal_places=2)
    promotion       = models.ForeignKey('Promotion', on_delete=models.SET_NULL, null=True)
    total_cost      = models.DecimalField(max_digits=10, decimal_places=2)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class Review(models.Model):
    order      = models.OneToOneField('Order', on_delete=models.CASCADE)
    rate       = models.DecimalField(max_digits=4, decimal_places=1)
    content    = models.CharField(max_length=1000)
    image_url  = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

class OrderProductStock(models.Model):
    order         = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_stock = models.ForeignKey('product.ProductStock', on_delete=models.CASCADE)
    quantity      = models.IntegerField()

    class Meta:
        db_table = 'order_product_stocks'

class OrderStatus(models.Model):
    id   = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'order_status'

class ShipmentStatus(models.Model):
    id   = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'shipment_status'
