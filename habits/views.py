from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Habit, HabitLog
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

#View pentru login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'habits/login.html', {'error': 'Invalid credentials'})
    return render(request, 'habits/login.html')

#View pentru register
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'habits/regsiter.html', {'error': 'Password do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'habits/register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'habits/register.html')

def home_view(request):
    return render(request, 'habits/home.html')

@login_required
def dashboard_view(request):
    habits = Habit.objects.filter(user=request.user)

    today = timezone.localdate()

    done_today_ids = set(
        HabitLog.objects.filter(
            habit__in=habits,
            date=today,
            done=True
        ).values_list("habit_id", flat=True)
    )

    days = [today - timezone.timedelta(days=i) for i in range(6, -1, -1)]

    streaks = {}
    for habit in habits:
        streak = 0
        for day in reversed(days):
            done = HabitLog.objects.filter(
                habit=habit,
                date=day,
                done=True
            ).exists()
            
            if done:
                streak += 1
            else:
                break
                
        streaks[habit.id] = streak

    habit_weekly = []
    for habit in habits:
        done_days = HabitLog.objects.filter(
            habit=habit,
            date__in=days,
            done=True
        ).count()

        habit_weekly.append({
            "habit":habit,
            "done_days":done_days,
            "total_days":len(days),
            "percent":int(done_days * 100/len(days)) if days else 0,
            "streak": streaks.get(habit.id, 0),
                          
        })

        habit_weekly.sort(key=lambda x: x["percent"], reverse=True)

    daily_counts = []
    for day in days:
        count = HabitLog.objects.filter(
            habit__in=habits,
            date=day,
            done=True
        ).count()
        daily_counts.append(count)

        daily_summary = list(zip(days, daily_counts))

    habit_rows = []
    for habit in habits:
        row_days = []
        for day in days:
            done = HabitLog.objects.filter(
                habit=habit,
                date=day,
                done=True
                ).count() > 0
            row_days.append(done)
             
            streak = 0
            for d in reversed(row_days):
                if d:
                    streak += 1
                else:
                    break

        habit_rows.append({
            "habit": habit,
            "days": row_days,
            "streak": streak,
        })

       
    return render(request, "habits/dashboard.html", {
        "habits": habits,
        "done_today_ids": done_today_ids,
        "days": days,
        "habit_rows": habit_rows,
        "daily_counts":daily_counts,
        "daily_summary": daily_summary,
        "habit_weekly":habit_weekly,
        "streaks": streaks,
    })

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def habit_create_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        target_daily = request.POST.get("target_daily")
        color = request.POST.get("color")

        Habit.objects.create(
            user=request.user,
            title=title,
            target_daily=target_daily,
            color=color
        )

        return redirect("dashboard")
    return render(request, "habits/habit_form.html")

@login_required
def habit_edit_view(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)

    if request.method == "POST":
        habit.title = request.POST.get("title")
        habit.target_daily = request.POST.get("target_daily")
        habit.color = request.POST.get("color")
        habit.save()
        return redirect("dashboard")
    
    return render(request, "habits/habit_form.html", {"habit":habit})

@login_required
def habit_delete_view(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)

    if request.method == "POST":
        habit.delete()
        return redirect("dashboard")

    return render(request, "habits/habit_confirm_delete.html", {"habit": habit})

@login_required
def habit_toggle_today_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.localdate()

    log = HabitLog.objects.filter(habit=habit, date=today).first()

    if log:
        log.delete()
    else:
        HabitLog.objects.create(habit=habit, date=today, done=True)

    return redirect("dashboard")

    @login_required
    def habit_detail_view(request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        today = timezone.localdate()
        days = [today - timedelta(days=i)
                for i in range(29, -1, -1)]
        logs = HabitLog.objects.filter(
            habit=habit,
            date__in=days,
            done=True)
        done_dates = set(logs.values_list("date", flat=True))
        days_statuses = [(day, day in done_dates) for day in days]
        total_done = HabitLog.objects.filter(habit=habit, done=True).count()
        streak = 0
        for day in reversed(days):
            if day in done_dates:
                streak += 1
            else:
                break

        return render(request, "habits/ habit_detail.html", {
            "habit": habit,
            "day_statuses": day_statuses,
            "total_done": total_done,
            "streak": streak,
        })
    