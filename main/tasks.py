import os
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from weasyprint import HTML
from .models import CV

@shared_task
def send_cv_pdf_via_email(cv_id, email_address):
    try:
        cv = CV.objects.get(pk=cv_id)
    except CV.DoesNotExist:
        return f"CV with id {cv_id} does not exist."

    # Render HTML template to string
    html_content = render_to_string("main/cv_detail_pdf.html", {"cv": cv})
    html_obj = HTML(string=html_content, base_url=settings.BASE_DIR)
    pdf_bytes = html_obj.write_pdf()

    subject = f"{cv.firstname} {cv.lastname} – CV PDF"
    body = f"Attached is the PDF for {cv.firstname} {cv.lastname}'s CV."
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_address],
    )

    filename = f"{cv.firstname}_{cv.lastname}_CV.pdf"
    email.attach(filename, pdf_bytes, "application/pdf")
    email.send()
    return f"PDF emailed to {email_address}."
