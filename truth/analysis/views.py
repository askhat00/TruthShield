from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import FileResponse, JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import AnalysisReport
from detector.main import SimpleDetector
import tempfile
import fitz  

@login_required
def reports_page(request):
    return render(request, 'detector/reports.html')

class AnalyzeTextView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        text = request.data.get("text","").strip()
        if not text:
            return Response({"error":"No text provided"}, status=400)

        detector = SimpleDetector.load()
        result = detector.analyze(text)

        report = AnalysisReport.objects.create(
            user=request.user,
            text=text,
            label=result['final_decision'],
            probability=result['probability'],
            sources=result['sources'],
            signs_of_falsification=result['signs_of_falsification']
        )

        return Response({
            "report_id": report.id,
            "text": text,
            "sources": result['sources'],
            "signs_of_falsification": result['signs_of_falsification'],
            "label": result['final_decision'],
            "probability": result['probability']
        })

class AnalyzeFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error":"No file uploaded"}, status=400)

        tmp_text = ""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        if file.name.endswith(".pdf"):
            doc = fitz.open(tmp_path)
            for page in doc:
                tmp_text += page.get_text()
            doc.close()
        else:
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                tmp_text = f.read()

        detector = SimpleDetector.load()
        result = detector.analyze(tmp_text)

        report = AnalysisReport.objects.create(
            user=request.user,
            text=tmp_text,
            file_name=file.name,
            label=result["final_decision"],
            probability=result["probability"],
            sources=result['sources'],
            signs_of_falsification=result['signs_of_falsification']
        )

        return Response({
            "report_id": report.id,
            "text": tmp_text,
            "sources": result['sources'],
            "signs_of_falsification": result['signs_of_falsification'],
            "label": result['final_decision'],
            "probability": result['probability']
        })

class ListReportsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = AnalysisReport.objects.filter(user=request.user).order_by('-created_at')
        data = [r.to_dict() for r in reports]
        return Response(data)

class ExportPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        try:
            report = AnalysisReport.objects.get(id=report_id, user=request.user)
        except AnalysisReport.DoesNotExist:
            return Response({"error":"Report not found"}, status=404)

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 800, "TruthShield Analysis Report")
        p.setFont("Helvetica", 12)
        y = 760
        for key, value in report.to_dict().items():
            if isinstance(value, list):
                value = ', '.join(value)
            p.drawString(50, y, f"{key}: {value}")
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"report_{report.id}.pdf")

class ExportJSONView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, report_id):
        try:
            report = AnalysisReport.objects.get(id=report_id, user=request.user)
        except AnalysisReport.DoesNotExist:
            return Response({"error":"Report not found"}, status=404)
        return JsonResponse(report.to_dict())
