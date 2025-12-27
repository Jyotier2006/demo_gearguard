from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.shortcuts import render, get_object_or_404, redirect
from .models import MaintenanceRequest

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def create_account(request):
    return render(request, 'create_account.html')
def home(request):
    return render(request, 'home.html')

def maintainance(request):
    requests = MaintenanceRequest.objects.all().order_by("-id")
    return render(request, "maintainance.html")


from django.shortcuts import get_object_or_404, redirect, render
from .models import MaintenanceRequest

def maintainance_detail(request, pk):
    req = get_object_or_404(MaintenanceRequest, pk=pk)

    if request.method == "POST":
        req.stage = request.POST.get("stage", req.stage)
        req.notes = request.POST.get("notes", req.notes)
        req.save()
        return redirect("maintainance_detail.html", pk=req.pk)  # ✅ prevents double submit

    return render(request, "maintainance_detail.html")




def about_us(request):
    return render(request, 'about_us.html')

def about_crops(request):
    return render(request, 'about_crops.html')

def logout_user(request):
    # Your logout logic here
    return render(request, 'logout.html')
from django.http import JsonResponse
from django.shortcuts import render

def evaluate_credit_score(request):
    if request.method == "POST":
        land_size = float(request.POST.get("land-size", 0))
        soil_health = int(request.POST.get("soil-health", 0))
        past_yield = float(request.POST.get("past-yield", 0))
        loan_amount = float(request.POST.get("loan-amount", 0))

        # Credit score formula
        credit_score = (land_size * 10) + (soil_health * 2) + (past_yield * 1.5) - (loan_amount / 1000)
        credit_score = max(0, min(credit_score, 100))

        # Determine risk level
        if credit_score > 80:
            risk_level = "Low Risk - Eligible for Loan"
        elif credit_score > 50:
            risk_level = "Medium Risk - Partial Loan"
        else:
            risk_level = "High Risk - Loan Denied"

        return JsonResponse({"credit_score": credit_score, "risk_level": risk_level})

    return render(request, "credit_score.html")
from django.shortcuts import render
from .models import MaintenanceRequest

from django.shortcuts import render
from .models import MaintenanceRequest

def dashboard(request):
    qs = MaintenanceRequest.objects.all().values(
        "id","subject","equipment","employee","technician",
        "category","maintenance_type","stage","scheduled_date",
        "request_date","company","duration_hours","notes"
    )
    return render(request, "dashboard.html", {"requests": list(qs)})

def home(request):
    return render(request, "home.html")
import json
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import MaintenanceRequest


def maintenance_calendar(request):
    # page only, events load via API
    return render(request, "maintenance_calendar.html")
def reporting(request):
    # page only, events load via API
    return render(request, "reporting.html")
def teams(request):
    # page only, events load via API
    return render(request, "teams.html")
def equipment(request):
    # page only, events load via API
    return render(request, "equipment.html")


@require_GET
def calendar_events(request):
    """
    FullCalendar will call:
      /api/calendar/events/?start=2025-12-01T00:00:00Z&end=2026-01-01T00:00:00Z
    We'll return JSON events.
    """
    start = request.GET.get("start")
    end = request.GET.get("end")

    # FullCalendar sends ISO datetimes; Django parse
    start_dt = parse_datetime(start) if start else None
    end_dt = parse_datetime(end) if end else None

    qs = MaintenanceRequest.objects.all()

    # Only scheduled items should appear on calendar
    qs = qs.exclude(scheduled_date__isnull=True)

    if start_dt and end_dt:
        # show events overlapping range (basic)
        qs = qs.filter(scheduled_date__gte=start_dt - timedelta(days=1),
                       scheduled_date__lte=end_dt + timedelta(days=1))

    # Optional filters from UI:
    stage = request.GET.get("stage")
    tech = request.GET.get("technician")
    mtype = request.GET.get("maintenance_type")
    if stage and stage != "all":
        qs = qs.filter(stage=stage)
    if tech and tech != "all":
        qs = qs.filter(technician=tech)
    if mtype and mtype != "all":
        qs = qs.filter(maintenance_type=mtype)

    events = []
    for r in qs:
        start_time = r.scheduled_date

        # duration_hours -> end
        dur = float(r.duration_hours or 0)
        end_time = start_time + timedelta(hours=dur) if dur > 0 else None

        events.append({
            "id": r.id,
            "title": f"{r.subject} • {r.equipment}",
            "start": start_time.isoformat(),
            "end": end_time.isoformat() if end_time else None,
            "extendedProps": {
                "subject": r.subject,
                "equipment": r.equipment,
                "employee": r.employee,
                "technician": r.technician,
                "category": r.category,
                "maintenance_type": r.maintenance_type,
                "stage": r.stage,
                "company": r.company,
                "priority": r.priority,
                "notes": r.notes,
                "duration_hours": float(r.duration_hours or 0),
            }
        })

    return JsonResponse(events, safe=False)


@csrf_exempt
@require_POST
def calendar_event_update(request, pk):
    """
    Update scheduled_date and/or duration_hours and/or stage, technician, notes
    Called on drag-drop or resize or modal save.
    """
    r = get_object_or_404(MaintenanceRequest, pk=pk)
    body = json.loads(request.body.decode("utf-8") or "{}")

    if "scheduled_date" in body:
        dt = parse_datetime(body["scheduled_date"])
        r.scheduled_date = dt

    if "duration_hours" in body:
        r.duration_hours = body["duration_hours"]

    for field in ["stage", "technician", "notes", "priority", "maintenance_type"]:
        if field in body:
            setattr(r, field, body[field])

    r.save()
    return JsonResponse({"ok": True})


@csrf_exempt
@require_POST
def calendar_event_create(request):
    """
    Create new request from calendar (Quick Add).
    """
    body = json.loads(request.body.decode("utf-8") or "{}")

    scheduled_date = parse_datetime(body.get("scheduled_date")) if body.get("scheduled_date") else None

    obj = MaintenanceRequest.objects.create(
        subject=body.get("subject", "Untitled"),
        equipment=body.get("equipment", ""),
        employee=body.get("employee", ""),
        technician=body.get("technician", ""),
        category=body.get("category", "it"),
        maintenance_type=body.get("maintenance_type", "corrective"),
        stage=body.get("stage", "new"),
        company=body.get("company", ""),
        priority=body.get("priority", "medium"),
        duration_hours=float(body.get("duration_hours", 1) or 1),
        scheduled_date=scheduled_date,
        notes=body.get("notes", ""),
    )

    return JsonResponse({"ok": True, "id": obj.id})
