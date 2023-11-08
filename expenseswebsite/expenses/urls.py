from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expenses'),
    path('edit-expense/<int:id>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<int:id>', views.delete_expense, name='expense-delete'),
    path('export-to-csv/', views.export_to_csv, name='export-to-csv'),
    path('export-to-excel/', views.export_to_excel, name='export-to-excel'),
    path('export-to-pdf/', views.export_to_pdf, name='export-to-pdf'),
]
