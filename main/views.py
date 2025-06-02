from django.shortcuts import render, get_object_or_404
from .models import CV
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

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
