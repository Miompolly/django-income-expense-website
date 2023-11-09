from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='income'),
    path('add-income', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.income_edit, name='income-edit'),
    path('income-delete/<int:id>', views.delete_income, name='income-delete'),
    path('export-to-csv/', views.export_to_csv, name='export-to-csv'),
    path('export-to-excel/', views.export_to_excel, name='export-to-excel'),
    path('export-to-pdf/', views.export_to_pdf, name='export-to-pdf'),
]
