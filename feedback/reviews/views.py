from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView, CreateView

from .models import Review
from .forms import ReviewForm


class ReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html" 
    success_url = "/thank-you"

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)
    


class ThankyouView(TemplateView):
    template_name = "reviews/thank_you.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['message'] = "This works!"
        return context
    

class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"

    def get_queryset(self):
        base =  super().get_queryset()
        # data = base.filter(rating__lte=3)
        return base

    


class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    model = Review



# ## Function Based View #####
    
# def review(request):
#     if request.method == "POST":
#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             # review = Review(user_name = form.cleaned_data['user_name'], review_text= form.cleaned_data['review_text'], rating= form.cleaned_data['rating'])
#             form.save()
#             return HttpResponseRedirect("/thank-you")
    
#     else:
#         form = ReviewForm()

#     return render(request, "reviews/review.html", {
#         "form": form
#         })


# def thank_you(request):
#     return render(request, "reviews/thank_you.html")