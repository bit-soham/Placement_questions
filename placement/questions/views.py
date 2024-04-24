from django.shortcuts import render # type: ignore
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # type: ignore
from .models import User, Companies, Tags, Questions
from django.utils.encoding import force_bytes, force_str # type: ignore
from django.contrib.auth.tokens import default_token_generator # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden # type: ignore
from django.urls import reverse # type: ignore
from django import forms # type: ignore
from django.conf import settings # type: ignore
from django.core.mail import send_mail # type:ignore
from django.contrib.sites.shortcuts import get_current_site # type: ignore
import socket
from django.contrib.auth.decorators import permission_required, login_required # type: ignore
from django.template.loader import render_to_string # type: ignore
from django.db import IntegrityError # type: ignore

# Create your views here.
# SECRET_KEY = 'c544efcf10d5ecf720c9318e460cb3c2270a9637f34641142df4b437d43857df'

class LoginForm(forms.Form):
    username = forms.CharField(strip=True, required=True, min_length=8, widget=forms.TextInput(attrs={ 'autofocus': True, 'class': 'login_username', 'placeholder': 'Username', 'autocomplete': 'off'}))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'login_password', 'placeholder': 'Password (min 8 char)', 'autocomplete': 'off'}))

class RegisterForm(forms.Form):
    username = forms.CharField(strip=True, required=True, min_length=8, widget=forms.TextInput(attrs={ 'autofocus': True, 'class': 'register_username', 'placeholder': 'Username', 'id': 'register_username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'register_email', 'id': 'register_email'}))                            
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'register_password', 'placeholder': 'Password (min 8 char)', 'id': 'register_password1'}))
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'class': 'register_confirm_password', 'placeholder': 'Confirm_password', 'id': 'register_password2'}))

class NewQuestionsForm(forms.ModelForm):
    class Meta: 
        model = Questions
        fields = ['question', 'image', 'company', 'tags', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4, 'cols':40, 'id': 'Qform_description' }),
            'image': forms.FileInput(attrs={'class': 'form-control Qform_image'}),
            'company': forms.CharField(),
            'tags': forms.TextInput(),
            'answer': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'id': 'Qform_answer' }),
        }
        
@login_required      
def index(request):
    companies = Companies.objects.all()
    return render(request, "questions/index.html", {
        'companies': companies
    })

def verify_email(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        token = force_str(urlsafe_base64_decode(token))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            # Mark the user's email as verified
            user.is_email_verified = True
            user.save()
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse("index") + "?ref=register")
            # return HttpResponse("Email verified successfully.")
        else:
            return HttpResponse("Email verification link is invalid.")
    except ():
        return HttpResponse("Email verification link is invalid.")
    
def company_questions(request, company):
    pass
def verify(request, user):
    if request.method == 'POST':
        pass
    else:
        return render("auctions/verify.html", {
            'user': user
        })
def image(request, image_id):
    question = Questions.objects.get(pk=image_id)
    if question.image:    
       image_url = f"{settings.MEDIA_URL}{question.image}"
    # Redirect the user to the image URL
       return HttpResponseRedirect(image_url)
        # return HttpResponseRedirect(reverse('display_image'), args=[image_id])
    else:
        raise Http404('Picture does not exist')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]      
            confirmation = form.cleaned_data["confirm_password"]

            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "questions/register.html", {
                    "message": "Passwords must match.",
                    "form": RegisterForm()
                })
            print("hello")
            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                token = default_token_generator.make_token(user)
                print("token",token)
                token = urlsafe_base64_encode(force_bytes(token))
                uid64 = urlsafe_base64_encode(force_bytes(user.id))
                verification_link = reverse('verify_email', args=[uid64, token])
                current_site = get_current_site(request)
                # print(verification_link)
                subject = 'Email Verification'
                message = 'Click the following link to verify your email: {0}'.format(verification_link)
                from_email = 'auction.ebay.gain@gmail.com'  # Replace with your email
                recipient_list = [user.email]
                # Create an HTML email using a template
                html_message = render_to_string('account/email/confirmation.html', {
                    'domain': current_site.domain,
                    'uid64': uid64,
                    'token': token,
                    'verification_link': verification_link,
                })
                for i in range(100):
                    try:
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
                        break
                    except socket.gaierror as e:
                        print(f"DNS ERROR {e} for the {i}th time")
                        if (i == 98):
                            initial_data = {
                                'username': username,
                                'email': email
                            }
                            return render(request, "questions/register.html", {
                                'form' : RegisterForm(initial=initial_data)
                            }) 
                    except Exception as e:
                        print(f"An error occurred {str(e)}")
                user.save()
                print("hello")
                return render(request, "questions/verify.html", {
                    'email': user.email,
                    'username': user.username
                })
            except IntegrityError:
                return render(request, "questions/register.html", {
                    "message": "Username already taken.",
                    "form": RegisterForm()
                })

        else:
            print("invalid form")
            return render(request, "questions/register.html", {
                'form': RegisterForm()
            })
        # return RegistrationView.as_view()(request)
    else:
        return render(request, "questions/register.html", {
            'form': RegisterForm()
        })

def login_view(request):
    # print("hello")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_email_verified:
                    login(request, user)
                    request.session['user_id'] = user.id
                    return HttpResponseRedirect(reverse("index"))   
                else:
                    return render(request, "questions/login.html", {
                        "message":"Please verify your email address before logging in.",
                        "form": LoginForm()
                    })
            else:
                return render(request, "questions/login.html", {
                    "message": "Invalid username and/or password.",
                    "form": LoginForm()
                })
        else:
            return render(request, "questions/login.html", {
                "form": LoginForm()
            })
    else:
        print("hello")
        return render(request, "questions/login.html", {
            "form": LoginForm()
        }) 
         
@login_required
def new_question(request):
    if request.method == 'POST':
        print("went to post")
        form = NewQuestionsForm(request.POST,request.FILES)
        print("got form")
        # raw_data = request.POST
        if form.is_valid():
            print("form is proved valid")
            # hashes = [hash.strip() for hash in item_hash.split(',') if hash.strip()]
            tags = form.cleaned_data["tags"]
            question = form.cleaned_data["question"]
            company = form.cleaned_data["company"]
            answer = form.cleaned_data["answer"]
            # parsed_datetime = datetime.strptime(last_bidding_datetime, '%m/%d/%Y %I:%M %p')
            image = form.cleaned_data["image"]
            user = request.user
            if not user: 
                return render(request, "questions/login.html", {
                    'message': 'you need to login to sell an item'
                })
            # hash_table = Hash_table.objects.all()
            tags = tags.split('#')
            Questions.objects.create(user=user, question=question, image=image, tags = tags, company=company, answer=answer)
            
            # item_instance.item_hash.add(*[Hash_table.objects.get_or_create(hash=hash)[0] for hash in hashes])
            # print(item_instance)
        else:
            print("form not valid")
            print(form.errors)
            for field, errors in form.errors.items():
                print(f"Field: {field}")
                for error in errors:
                    print(f"errors: {error}")
                    field_instance = form.fields[field]
                    if hasattr(field_instance, 'error_messages'):
                        expected_format = field_instance
                        print(f"Excepted formatter: {expected_format}")
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "questions/new_question.html", {
            "forms": NewQuestionsForm()
        })
def  logout_view(request):
    request.session.clear()
    logout(request)
    return HttpResponseRedirect(reverse("index"))