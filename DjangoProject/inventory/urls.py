from django.urls import path
from . import views, auth_views

app_name = "inventory"

urlpatterns = [
    # Home / Book List — All users
    path("", views.book_list, name="book_list"),
    # Book CRUD — Staff only
    path("books/add/", views.add_book, name="add_book"),
    path("books/<int:pk>/edit/", views.edit_book, name="edit_book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete_book"),
    path("books/<int:pk>/", views.view_book, name="view_book"),
    # Issue / Return Books — Logged-in users
    path("books/<int:book_id>/issue/", views.issue_book, name="issue_book"),
    path(
        "transactions/<int:transaction_id>/return/",
        views.return_book,
        name="return_book",
    ),
    # User-specific books
    path("my-books/", views.my_books, name="my_books"),
    # Staff dashboard
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),
    # Authentication
    path("signup/", auth_views.signup_view, name="signup"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
]
