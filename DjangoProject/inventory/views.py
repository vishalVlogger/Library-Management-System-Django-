from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Book, Transaction, Member
from .forms import BookForm
from django.utils import timezone

# READ — All users can view books
@login_required
def book_list(request):
    query = request.GET.get("q")
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()
    return render(request, "inventory/book_list.html", {"books": books})

# CREATE
@login_required
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        book = form.save()
        messages.success(request, f"Book '{book.title}' added successfully.")
        # Redirect to edit page to see the saved form
        return redirect("inventory:staff_dashboard")
    return render(
        request, "inventory/book_form.html", {"form": form, "title": "Add Book"}
    )

# UPDATE
@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, f"✏️ Book '{book.title}' updated successfully.")
        return redirect(
            "inventory:staff_dashboard"
        )  # Redirect to staff dashboard after save
    return render(
        request,
        "inventory/book_form.html",
        {"form": form, "title": "Edit Book"},
    )

# DELETE
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, f"Book '{book.title}' deleted successfully.")
        return redirect("inventory:staff_dashboard")
    return render(request, "inventory/book_confirm_delete.html", {"book": book})

@login_required
def view_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "inventory/book_detail.html", {"book": book})

@login_required
def issue_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    member, _ = Member.objects.get_or_create(
        user=request.user,
        defaults={"membership_id": f"M{request.user.id:04d}", "active": True},
    )

    if book.available_quantity <= 0:
        messages.error(request, f"Cannot issue '{book.title}': Out of stock.")
        return redirect("inventory:book_list")

    Transaction.objects.create(
        member=member,
        book=book,
        transaction_type="ISSUE",
        quantity=1,
        issue_date=timezone.localtime(timezone.now()),
    )

    book.available_quantity -= 1
    book.save(update_fields=["available_quantity"])

    messages.success(request, f"You have successfully issued '{book.title}'.")
    return redirect("inventory:my_books")

@login_required
def return_book(request, transaction_id):
    txn = get_object_or_404(Transaction, id=transaction_id, member__user=request.user)

    if txn.transaction_type == "RETURN":
        messages.info(request, f"'{txn.book.title}' is already returned.")
        return redirect("inventory:my_books")

    txn.transaction_type = "RETURN"
    txn.return_date = timezone.localtime(timezone.now())
    txn.save(update_fields=["transaction_type", "return_date"])

    book = txn.book
    book.available_quantity = min(
        book.available_quantity + txn.quantity, book.total_quantity
    )
    book.save(update_fields=["available_quantity"])

    messages.success(request, f"You have successfully returned '{book.title}'.")
    return redirect("inventory:my_books")

@login_required
def my_books(request):
    member = Member.objects.filter(user=request.user).first()
    if not member:
        messages.warning(request, "You don't have any transactions yet.")
        return redirect("inventory:book_list")

    transactions = member.transactions.select_related("book").order_by("-issue_date")
    return render(request, "inventory/my_books.html", {"transactions": transactions})

@staff_member_required
def staff_dashboard(request):
    books = Book.objects.all()
    users = User.objects.all()
    transactions = Transaction.objects.select_related(
        "book", "member", "member__user"
    ).order_by("-issue_date")
    return render(
        request,
        "inventory/staff_dashboard.html",
        {"books": books, "users": users, "transactions": transactions},
    )