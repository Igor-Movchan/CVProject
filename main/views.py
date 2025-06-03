from django.shortcuts import render, get_object_or_404, redirect
from .models import CV
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import RequestLog
from django.urls import reverse
from django.contrib import messages
from .tasks import send_cv_pdf_via_email
import os
import openai

# List of supported languages
TRANSLATION_LANGUAGES = [
    ("kw", "Cornish"),
    ("gv", "Manx"),
    ("br", "Breton"),
    ("iu", "Inuktitut"),
    ("kl", "Kalaallisut"),
    ("rmy", "Romani"),
    ("oc", "Occitan"),
    ("lad", "Ladino"),
    ("se", "Northern Sami"),
    ("hsb", "Upper Sorbian"),
    ("csb", "Kashubian"),
    ("zza", "Zazaki"),
    ("cv", "Chuvash"),
    ("liv", "Livonian"),
    ("tsak", "Tsakonian"),
    ("srm", "Saramaccan"),
    ("bi", "Bislama"),
]

LANGUAGE_DICT = dict(TRANSLATION_LANGUAGES)

def recent_requests(request):
    logs = RequestLog.objects.order_by("-timestamp")[:10]
    return render(request, "main/logs.html", {"logs": logs})

def cv_pdf(request, pk):
    # Fetch the CV instance or return 404
    cv = get_object_or_404(CV, pk=pk)

    # Render the HTML template with context
    html_string = render_to_string("main/cv_detail_pdf.html", {"cv": cv})

    # Generate the PDF
    pdf_file = weasyprint.HTML(string=html_string).write_pdf()

    # Create a response with the PDF as an attachment
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=cv_{cv.id}.pdf"

    return response

def cv_list(request):
    cvs = CV.objects.all()
    return render(request, "main/cv_list.html", {"cvs": cvs})

def cv_detail(request, pk):
    cv = CV.objects.get(pk=pk)
    context = {
        "cv": cv,
        "translation_languages": TRANSLATION_LANGUAGES,
    }

    if "translated_content" in request.GET:
        context["translated_content"] = request.GET["translated_content"]
        code = request.GET.get("target_language", "")
        context["selected_language_name"] = LANGUAGE_DICT.get(code, "")
        context["translation_languages"] = TRANSLATION_LANGUAGES

    return render(request, "main/cv_detail.html", context)

def cv_translate(request, pk):
    if request.method != "POST":
        return redirect(reverse("cv_detail", args=[pk]))

    target_language_code = request.POST.get("target_language")
    target_language_name = LANGUAGE_DICT.get(target_language_code, "")

    if not target_language_code:
        messages.error(request, "Please select a language.")
        return redirect(reverse("cv_detail", args=[pk]))

    try:
        cv = CV.objects.get(pk=pk)
    except CV.DoesNotExist:
        messages.error(request, f"CV with id {pk} does not exist.")
        return redirect(reverse("cv_list"))

    cv_text = f"""\
    First name: {cv.firstname}
    Last name: {cv.lastname}
    Bio: {cv.bio}
    Skills: {cv.skills}
    Projects: {cv.projects}
    Contacts: {cv.contacts}
    """
    prompt = (
        f"Translate the following CV text into {target_language_name}. "
        f"Preserve formatting as plain text:\n\n{cv_text}"
    )

    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates text."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        translated = response.choices[0].message.content.strip()
    except Exception as e:
        messages.error(request, f"Translation failed: {str(e)}")
        return redirect(reverse("cv_detail", args=[pk]))

    from urllib.parse import urlencode

    params = {
        "translated_content": translated,
        "target_language": target_language_code,
    }
    query_string = urlencode(params)
    return redirect(f"{reverse('cv_detail', args=[pk])}?{query_string}")

def settings_view(request):
    return render(request, "main/settings.html")

def send_cv_email(request, pk):
    if request.method == "POST":
        email_address = request.POST.get("email")
        send_cv_pdf_via_email.delay(pk, email_address)
        messages.info(request, f"PDF will be emailed to {email_address}.")
    return redirect(reverse("cv_detail", args=[pk]))


