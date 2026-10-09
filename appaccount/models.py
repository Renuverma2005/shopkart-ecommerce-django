from django.db import models



class Category(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    
    
    
    
    
    








class Product(models.Model):

    name = models.CharField(max_length=200)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    
    subcategory = models.ForeignKey(
        'SubCategory',
        on_delete=models.CASCADE,
        related_name='products',
        blank=True,
        null=True
    ) 
   
                               

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    # Product Price
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Old Price
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Short Description
    short_description = models.CharField(
        max_length=300,
        blank=True
    )

    # Full Description
    description = models.TextField()

    # Product Color
    color = models.CharField(
        max_length=100,
        blank=True
    )

    # Product Size
    size = models.CharField(
        max_length=100,
        blank=True
    )

    # Gender
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Unisex', 'Unisex'),
        ('Kids', 'Kids'),
    ]

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='Unisex'
    )

    # Product Available
    available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def discount_percentage(self):

        if self.old_price and self.old_price > self.price:
            return round(
                ((self.old_price - self.price) / self.old_price) * 100
            )

        return 0

    def __str__(self):
        return self.name








class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    name = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='subcategories/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        ordering = ['name']




# checkout.html page start here
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cod', 'Cash on Delivery'),
        ],
        default='cod'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    class Meta:
        ordering = ['-created_at']










class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"

