from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Member(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class IssueBook(models.Model):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    issue_date = models.DateField(
        auto_now_add=True
    )

    due_date = models.DateField()

    return_date = models.DateField(
        null=True,
        blank=True
    )

    returned = models.BooleanField(
        default=False
    )

    fine = models.IntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.book.title} - {self.member.name}"
