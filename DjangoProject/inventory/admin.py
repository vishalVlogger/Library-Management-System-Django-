from django.contrib import admin
from .models import Category, Book, Transaction, Member


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "authors",
        "category",
        "available_quantity",
        "total_quantity",
    )
    search_fields = ("title", "authors", "isbn", "publisher")
    list_filter = ("category",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("membership_id", "user", "phone", "active")
    search_fields = ("membership_id", "user__username", "user__email")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "member",
        "transaction_type",
        "issue_date",
        "due_date",
        "return_date",
        "quantity",
    )
    search_fields = ("book__title", "member__membership_id", "member__user__username")
    list_filter = ("transaction_type",)
