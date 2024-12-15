import csv
from django.shortcuts import render
from django.contrib import messages
from .models import Employee, Company
from .forms import EmployeeUploadForm

# Function to upload employees from a CSV file
def upload_employees(request):
    if request.method == 'POST':
        form = EmployeeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the user has a company assigned
            if not hasattr(request.user, 'company') or request.user.company is None:
                messages.error(request, "You are not associated with any company. Please contact your administrator.")
                return render(request, 'employees/upload.html', {'form': form})

            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            added, updated = 0, 0
            for row in reader:
                try:
                    employee, created = Employee.objects.update_or_create(
                        email=row['email'],
                        defaults={
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'role': row['role'],
                            'company': request.user.company,  # Assign the user's company
                        }
                    )
                    if created:
                        added += 1
                    else:
                        updated += 1
                except Exception as e:
                    messages.error(request, f"Error processing row {row}: {e}")

            messages.success(request, f"{added} employees added, {updated} employees updated.")
    else:
        form = EmployeeUploadForm()

    return render(request, 'employees/upload.html', {'form': form})

# Add the API viewset for Employee
from rest_framework.viewsets import ModelViewSet
from .serializers import EmployeeSerializer

# Employee ViewSet for API routes
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

