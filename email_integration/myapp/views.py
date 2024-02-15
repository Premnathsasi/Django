from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db.models import F 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from .forms import ContactForm, LoginForm, SignupForm, UserProfileUpdateForm
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from .models import Product, CartItem, Cart

members_list = [
    {
        "image": "person_1.jpg",
        "name": "Lawson Arnold",
        "designation": "CEO, Founder, Atty.",
        "headline": "Separated they live in. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean."
    },
    {
        "image": "person_2.jpg",
        "name": "Jeremy Walker",
        "designation": "CEO, Founder, Atty.",
        "headline": "Separated they live in. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean."
    },
    {
        "image": "person_3.jpg",
        "name": "Patrik Wilson",
        "designation": "CEO, Founder, Atty.",
        "headline": "Separated they live in. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean."
    },
    {
        "image": "person_4.jpg",
        "name": "Kathryn Heigh",
        "designation": "CEO, Founder, Atty.",
        "headline": "Separated they live in. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean."
    },
]

class BaseView(View):
    def get_cart_count(self, user):
        if user.is_authenticated and hasattr(user, 'cart'):
            return user.cart.items.all().count()
        return 0



class HomeView(BaseView):
    def get(self, request):
        products = Product.objects.all()[:3]
        cart_count = self.get_cart_count(request.user)
        return render(request, "myapp/home.html", {
            "is_loggedin": request.user.is_authenticated,
            "is_active": 'home',
            "products": products,
            'cart_count': cart_count
        })


class AboutView(BaseView):
    def get(self, request):
        cart_count = self.get_cart_count(request.user)
        return render(request, "myapp/about.html", {
            "is_active": "about",
            "is_loggedin": request.user.is_authenticated,
            'members': members_list,
            'cart_count': cart_count
        })


class ShopView(BaseView):
    def get(self, request):
        products = Product.objects.all()
        cart_count = self.get_cart_count(request.user)
        return render(request, "myapp/shop.html", {
            "is_loggedin": request.user.is_authenticated,
            "is_active": 'shop',
            "products": products,
            'cart_count': cart_count
        })


class ProductDetailView(BaseView):
    def get(self, request, slug):
        cart_count = self.get_cart_count(request.user)
        product = Product.objects.get(slug=slug)
        return render(request, "myapp/product_detail.html", {
            "is_loggedin": request.user.is_authenticated, 
            "product": product, 
            'cart_count': cart_count 
        })

class CartView(View):
    def get(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'cart'):
            cart_instance = request.user.cart
            cart_items = cart_instance.items.all()
            cart_count = cart_items.count()
            total_cost = cart_instance.total_cost()
        else:
            cart_count = 0
            cart_items = []
            total_cost = 0

        return render(request, "myapp/cart.html", {"is_loggedin": request.user.is_authenticated, 'cart_count': cart_count, 'cart_items': cart_items, "total_cost": total_cost})

    def post(self, request):
        return self.get(request)

class ContactView(BaseView):
    def get(self, request):
        cart_count = self.get_cart_count(request.user)
        form = ContactForm()
        return render(request, "myapp/contact.html", {'form': form, "is_loggedin": request.user.is_authenticated, "is_active": 'contact', 'cart_count': cart_count})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Sending email using Sendinblue Python SDK
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration))
            subject = f"New Message from {name}"
            sender = {"name": name, "email": email}
            html_content = f"""<html>
            <style>
                table, th, td {{
                    border: 1px solid black;
                    border-collapse: collapse;
                    padding:5px;
                    }}
            </style>
            <body>
            <h2>Customer Details</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Message</th>
                </tr>
                <tr>
                <td>{name}</td>
                <td>{email}</td>
                <td>{message}</td>
                </tr>
            </table>
            </body>
            </html>"""
            to = [{"email": "premnath@cedillainteractive.com", "name": "Premnath"}]
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to, subject=subject, sender=sender, html_content=html_content)

            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                print(api_response)
                return render(request, 'myapp/thank-you.html')
            except ApiException as e:
                return HttpResponse(f"Exception when calling SMTPApi->send_transac_email: {e}\n")
        return render(request, "myapp/contact.html", {'form': form})


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "myapp/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                error_message = "Invalid username or password. Please try again."
        else:
            error_message = "An error occurred. Please check your input and try again."

        return render(request, "myapp/login.html", {"form": form, "error_message": error_message})


class UserSignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "myapp/signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, "myapp/signup.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


class UpdateProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
            
        else:
            if request.user.is_authenticated and hasattr(request.user, 'cart'):
                cart_count = request.user.cart.items.all().count()
            else:
                cart_count = 0
            form = UserProfileUpdateForm(instance=request.user)
            return render(request, "myapp/update_profile.html", {'form': form, "is_loggedin": request.user.is_authenticated,"is_active": 'profile', 'cart_count': cart_count})
            
    def post(self, request):
        form = UserProfileUpdateForm(request.POST, instance= request.user)
        if form.is_valid():
            form.save()
            return redirect("update-profile")
        else:
            return render(request, "myapp/update_profile.html", {'form': form, "is_loggedin": request.user.is_authenticated,"is_active": 'profile'})

class AddToCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                product_id = request.POST.get('product_id')
                quantity = int(request.POST.get('quantity', 1))

                product = get_object_or_404(Product, pk=product_id)
                cart, created = Cart.objects.get_or_create(user=request.user)

            # Check if the product already exists in the cart
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            # If the product already exists in the cart, update the quantity
                if not created:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity = quantity

                cart_item.save()

            # Calculate the total number of items in the cart
                total_items = CartItem.objects.filter(cart=cart).count()

                return JsonResponse({'success': True, 'cart_number': total_items})
            else:
                return JsonResponse({'success': False})
        else:
            return JsonResponse({'sucess': False, 'message': "Please login"})


def delete_from_cart(request, pk):
    if request.method == 'DELETE':
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    else:
        # Return a 405 Method Not Allowed response for other HTTP methods
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)



class UpdateCartItemView(View):
    def post(self, request, id):
        new_quantity = int(request.POST.get('quantity'))

        cart_item = get_object_or_404(CartItem, id=id)
        old_quantity = cart_item.quantity

        cart_item.quantity = new_quantity
        cart_item.save()
        total_cost = cart_item.total_cost()
        
        cart = cart_item.cart
        updated_total_cost = cart.total_cost()
        
        return JsonResponse({'total_cost': total_cost, 'cart_total': updated_total_cost})
    