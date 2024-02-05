from django.shortcuts import get_object_or_404, render
from django.http import Http404 
from django.db.models import Avg

from .models import Book

# Create your views here.
def index(request):
    all_books = Book.objects.all().order_by("title") # (-) before value is used to sort in descending order
    num_books = all_books.count() #Count is used to find total number of entries in the book model
    avg_rating = all_books.aggregate(Avg("rating")) # aggregate is used to find out the aggregated avg value of the table

    return render(request, "book_outlet/index.html",{
        'books': all_books,
        'total_Books': num_books,
        'avg_rating': avg_rating,

    } )

def book_detail(request, slug):
    # try:
    #     book = Book.objects.get(pk=id)
    # except:
    #     raise Http404()
    book = get_object_or_404(Book, slug=slug)
    return render(request, "book_outlet/book_detail.html", {
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestselling": book.is_bestselling,
    })