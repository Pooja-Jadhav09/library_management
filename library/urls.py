from django.urls import path
from . import views

urlpatterns = [

    path("",views.dashboard,name="dashboard"),

    path("books/",views.book_list,name="book_list"),

    path("add/",views.add_book,name="add_book"),

    path("update/<int:id>/",views.update_book,name="update_book"),

    path("delete/<int:id>/",views.delete_book,name="delete_book"),

    path("members/",views.member_list,name="member_list"),

    path("add-member/",views.add_member,name="add_member"),

    path("update-member/<int:id>/",views.update_member,name="update_member"),

    path("delete-member/<int:id>/",views.delete_member,name="delete_member"),

    path("issue-book/",views.issue_book,name="issue_book"),

    path("issued-books/",views.issued_books,name="issued_books"),

    path("return-book/<int:id>/",views.return_book,name="return_book"),

    path("signup/",views.signup_user,name="signup"),

    path("login/",views.login_user,name="login"),

    path("logout/",views.logout_user,name="logout"),
]