from django.urls import path
from .views import (
    reports_page,
    AnalyzeTextView,
    AnalyzeFileView,
    ListReportsView,
    ExportPDFView,
    ExportJSONView
)

urlpatterns = [
    path('analyze-text/', AnalyzeTextView.as_view(), name='analyze_text'),
    path('analyze-file/', AnalyzeFileView.as_view(), name='analyze_file'),
    path('reports/', reports_page, name='reports_page'),
    path('api/reports/', ListReportsView.as_view(), name='list_reports'),
    path('api/report/<int:report_id>/pdf/', ExportPDFView.as_view(), name='export_pdf'),
    path('api/report/<int:report_id>/json/', ExportJSONView.as_view(), name='export_json'),
]
