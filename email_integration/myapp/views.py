from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Sending email using Sendinblue Python SDK
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = f"New Message from {name}"
            sender = {"name": name, "email": email}
            html_content = f"<html><body><h3>{message}</h3></body></html>"
            to = [{"email": "premnath@cedillainteractive.com", "name": "Premnath"}]
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, subject=subject, sender=sender, html_content=html_content)

            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                print(api_response)
                return render(request, 'myapp/thank-you.html')
            except ApiException as e:
                return HttpResponse(f"Exception when calling SMTPApi->send_transac_email: {e}\n")

    else:
        form = ContactForm()
    return render(request, "myapp/home.html", {'form': form})
