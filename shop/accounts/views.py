from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from accounts.forms import RegistrationForm
from accounts.models import Account
from accounts.utils import _profile, _redirect_to_next_page
from carts.utils import _move_cart_when_authenticate
from shop.emails import Emails


class RegisterView(CreateView):
    """View for registration in the site."""
    form_class = RegistrationForm
    model = Account

    def get(self, request, *args, **kwargs):
        """Render the register template."""
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        """
        Register for new user and after create profile
        for him and sending email. Try to move his cart
        items to new cart.
        """
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            # create new user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name,
                                               last_name=last_name,
                                               email=email,
                                               password=password)
            user.phone_number = phone_number

            # Create profile for user and save it
            _profile(user)
            user.save()

            # Email confirmation
            Emails(user=user, email=email, pk=user.pk)

            user = auth.authenticate(request=request, email=email, password=password)

            # Login user and move his cart
            if user is not None:
                _move_cart_when_authenticate(request, user)
                auth.login(request, user)
                return redirect('category_main')
        context = {'form': form}
        return render(request, 'accounts/register.html', context)


class LoginView(View):

    """View for logging in the site."""
    def get(self, request, *args, **kwargs):
        """Render the login template."""
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        """
        Authentication and authorization code,
        gets email and password, if authentication
        success tried to redirect to 'next' page
        and move a cart to authorized user.
        """
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request=request, username=email, password=password)

        # login user and move his cart
        if user is not None:
            _move_cart_when_authenticate(request, user)
            auth.login(request, user)
            try:
                _redirect_to_next_page(request)
            except:
                return redirect('store')

        else:
            messages.error(request, 'Неправильно введена почта или пароль')
            return redirect('login')


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        """Logout view, only for has already logged in users."""
        auth.logout(request)
        messages.success(request, 'Вы успешно вышли из системы')
        return redirect('login')


class ConfirmAccountView(View):

    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64']).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.email = email
            user.confirm_email = True
            user.save()
            messages.success(request, 'Congratulations! Your account is activated.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link')
            return redirect('register')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')