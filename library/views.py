from django.shortcuts import render, redirect
from .models import Book, Member, IssueBook, Category

from django.contrib.auth.models import User,Group
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from datetime import date
from django.db.models import Sum


def signup_user(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = User.objects.create_user(
         username=username,
         password=password
        )

        group = Group.objects.get(
        name="user"
        )

        user.groups.add(group)
        return redirect("login")

    return render(
        request,
        "signup.html"
    )
    
def login_user(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                "dashboard"
            )

    return render(
        request,
        "login.html"
    )
    
def logout_user(request):

        logout(request)

        return redirect(
        "login"
    )
        
@login_required
def dashboard(request):

    total_book_titles = Book.objects.count()

    total_books = Book.objects.aggregate(
    Sum("quantity")
)["quantity__sum"] or 0

    total_members = Member.objects.count()

    issued_books = IssueBook.objects.filter(
        returned=False
    ).count()

    returned_books = IssueBook.objects.filter(
        returned=True
    ).count()

    overdue_books = IssueBook.objects.filter(
        due_date__lt=date.today(),
        returned=False
    ).count()

    role = request.user.groups.first()

    context = {
        "total_book_titles": total_book_titles,
        "total_books": total_books,

        "total_members": total_members,

        "issued_books": issued_books,

        "returned_books": returned_books,

        "overdue_books": overdue_books,

        "role": role,
    }

    return render(
        request,
        "dashboard.html",
        context
    )
@login_required   
def add_book(request):

    if not request.user.groups.filter(
        name="admin"
    ).exists():

        messages.error(
            request,
            "Only Admin can add books."
        )

        return redirect(
            "book_list"
        )

    if request.method == "POST":

        title = request.POST.get(
            "title"
        )

        author = request.POST.get(
            "author"
        )

        isbn = request.POST.get(
            "isbn"
        )

        quantity = request.POST.get(
            "quantity"
        )

        category_id = request.POST.get(
            "category"
        )

        category = Category.objects.get(
            id=category_id
        )

        Book.objects.create(
            category=category,
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity
        )

        messages.success(
            request,
            "Book added successfully."
        )

        return redirect(
            "book_list"
        )

    categories = Category.objects.all()

    role = request.user.groups.first()

    return render(
        request,
        "add_book.html",
        {
            "categories": categories,
            "role": role
        }
    )
@login_required   
def book_list(request):

    search = request.GET.get(
        "search"
    )

    category_id = request.GET.get(
        "category"
    )

    books = Book.objects.all()

    if search:

        books = books.filter(
            title__icontains=search
        )

    if category_id:

        books = books.filter(
            category_id=category_id
        )

    categories = Category.objects.all()

    role = request.user.groups.first()

    return render(
        request,
        "book_list.html",
        {
            "books": books,
            "categories": categories,
            "role": role
        }
    )
@login_required   
def update_book(request, id):
    if request.user.groups.filter(
         name="user"
        ).exists():

        messages.error(
            request,
            "Access Denied."
        )

        return redirect("book_list")

    book = Book.objects.get(
        id=id
    )

    if request.method == "POST":

        book.title = request.POST.get(
            "title"
        )

        book.author = request.POST.get(
            "author"
        )

        book.isbn = request.POST.get(
            "isbn"
        )

        book.quantity = request.POST.get(
            "quantity"
        )

        book.save()

        messages.success(
            request,
            "Book updated successfully."
        )

        return redirect(
            "book_list"
        )

    return render(
        request,
        "update_book.html",
        {
            "book": book
        }
    )
@login_required    
def delete_book(request, id):

    if not request.user.groups.filter(
        name="admin"
    ).exists():

        messages.error(
            request,
            "Only Admin can delete books."
        )

        return redirect(
            "book_list"
        )

    book = Book.objects.get(
        id=id
    )

    book.delete()

    messages.success(
        request,
        "Book deleted successfully."
    )

    return redirect(
        "book_list"
    )
@login_required    
def add_member(request):

    if not request.user.groups.filter(
        name="admin"
    ).exists():

        messages.error(
            request,
            "Only Admin can add members."
        )

        return redirect(
            "member_list"
        )

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        email = request.POST.get(
            "email"
        )

        phone = request.POST.get(
            "phone"
        )

        Member.objects.create(
            name=name,
            email=email,
            phone=phone
        )

        messages.success(
            request,
            "Member added successfully."
        )

        return redirect(
            "member_list"
        )

    role = request.user.groups.first()

    return render(
        request,
        "add_member.html",
        {
            "role": role
        }
    )
@login_required   
def member_list(request):
    if request.user.groups.filter(
        name="user"
    ).exists():

        messages.error(
            request,
            "Access Denied."
        )

        return redirect("dashboard")

    members = Member.objects.all()

    role = request.user.groups.first()

    return render(
        request,
        "member_list.html",
        {
            "members": members,
            "role": role
        }
    )
@login_required    
def update_member(request, id):

    member = Member.objects.get(
        id=id
    )

    if request.method == "POST":

        member.name = request.POST.get(
            "name"
        )

        member.email = request.POST.get(
            "email"
        )

        member.phone = request.POST.get(
            "phone"
        )

        member.save()

        messages.success(
            request,
            "Member updated successfully."
        )

        return redirect(
            "member_list"
        )

    return render(
        request,
        "update_member.html",
        {
            "member": member
        }
    )
@login_required   
def delete_member(request, id):

    if not request.user.groups.filter(
        name="admin"
    ).exists():

        messages.error(
            request,
            "Only Admin can delete members."
        )

        return redirect(
            "member_list"
        )

    member = Member.objects.get(
        id=id
    )

    member.delete()

    messages.success(
        request,
        "Member deleted successfully."
    )

    return redirect(
        "member_list"
    )
@login_required    
def issue_book(request):

    if request.method == "POST":

        book_id = request.POST.get(
            "book"
        )

        member_id = request.POST.get(
            "member"
        )

        due_date = request.POST.get(
            "due_date"
        )

        book = Book.objects.get(
            id=book_id
        )

        member = Member.objects.get(
            id=member_id
        )

        existing_issue = IssueBook.objects.filter(
            book=book,
            member=member,
            returned=False
        ).exists()

        if existing_issue:

            messages.error(
                request,
                "This member already has this book issued."
            )

            return redirect(
                "issue_book"
            )

        if book.quantity > 0:

            IssueBook.objects.create(
                book=book,
                member=member,
                due_date=due_date
            )

            book.quantity -= 1

            book.save()

            messages.success(
                request,
                "Book issued successfully."
            )

        else:

            messages.error(
                request,
                "Book is out of stock."
            )

        return redirect(
            "issued_books"
        )

    books = Book.objects.all()

    members = Member.objects.all()

    role = request.user.groups.first()

    return render(
        request,
        "issue_book.html",
        {
            "books": books,
            "members": members,
            "role": role
        }
    )
@login_required   
def issued_books(request):

    issued = IssueBook.objects.all()

    role = request.user.groups.first()

    return render(
        request,
        "issued_books.html",
        {
            "issued": issued,
            "role": role
        }
    )
@login_required   
def return_book(request, id):

    issue = IssueBook.objects.get(
        id=id
    )

    if not issue.returned:

        today = date.today()

        late_days = (
            today - issue.due_date
        ).days

        if late_days > 0:

            issue.fine = late_days * 10

        issue.return_date = date.today()

        issue.returned = True

        issue.save()

        issue.book.quantity += 1

        issue.book.save()

        messages.success(
            request,
            f"Book returned successfully. Fine: ₹{issue.fine}"
        )

    return redirect(
        "issued_books"
    )