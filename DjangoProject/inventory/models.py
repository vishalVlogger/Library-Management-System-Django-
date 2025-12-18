from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    authors = models.CharField(
        max_length=255, help_text="Comma-separated list of authors"
    )
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True)
    publisher = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books"
    )
    description = models.TextField(blank=True)
    total_quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(0)]
    )
    available_quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    add_on = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)

    class Meta:
        ordering = ["title"]
        unique_together = (("title", "authors", "publisher"),)

    def __str__(self):
        return f"{self.title} by {self.authors}"

    def compute_available(self):
        return self.available_quantity

    def adjust_stock(self, delta):
        """
        Adjust available_quantity by delta (negative to issue, positive to return).
        Use carefully from views/transaction logic.
        """
        new = self.available_quantity + delta
        if new < 0:
            raise ValueError("Insufficient stock to issue the requested quantity.")
        self.available_quantity = new
        self.save(update_fields=["available_quantity"])


class Member(models.Model):
    # Link to Django user to reuse authentication
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member_profile"
    )
    membership_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username} ({self.membership_id})"
        )


class Transaction(models.Model):
    ISSUE = "ISSUE"
    RETURN = "RETURN"
    TRANSACTION_TYPES = [
        (ISSUE, "Issue"),
        (RETURN, "Return"),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="transactions"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.transaction_type} - {self.book.title} * {self.quantity} to {self.member.membership_id}"

    def save(self, *args, **kwargs):
        """
        Override save to adjust book.available_quantity.
        IMPORTANT: This is a simple approach — for production consider
        transactional operations (atomic) and better handling for edits.
        """

        created = self.pk is None
        # If creating a new transaction:
        if created:
            if self.transaction_type == Transaction.ISSUE:
                # make sure enough stock
                if self.book.available_quantity < self.quantity:
                    raise ValueError(
                        "Insufficient stock to issue the requested quantity."
                    )
                self.book.available_quantity -= self.quantity
                self.book.save(update_fields=["available_quantity"])
            elif self.transaction_type == Transaction.RETURN:
                self.book.available_quantity += self.quantity
                self.book.save(update_fields=["available_quantity"])
        else:
            # For updates, more complex logic would be needed to adjust stock correctly.
            pass
        super().save(*args, **kwargs)


class Profile(models.Model):
    ROLE_CHOICES = [("STAFF", "Staff"), ("USER", "User")]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    def __str__(self):
        return f"{self.user.username} - {self.role}"