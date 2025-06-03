from django.shortcuts import render, get_object_or_404, redirect
from .models import CV
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from .models import RequestLog
from django.urls import reverse
from django.contrib import messages
from .tasks import send_cv_pdf_via_email

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
    cv = get_object_or_404(CV, pk=pk)
    return render(request, "main/cv_detail.html", {"cv": cv})

def settings_view(request):
    return render(request, "main/settings.html")

def send_cv_email(request, pk):
    if request.method == "POST":
        email_address = request.POST.get("email")
        send_cv_pdf_via_email.delay(pk, email_address)
        messages.info(request, f"PDF will be emailed to {email_address}.")
    return redirect(reverse("cv_detail", args=[pk]))


