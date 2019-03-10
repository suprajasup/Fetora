from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User 
from fees.models import Profile,FeeHistory
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# Create your views here.
def home(request):
	return render(request,"home.html")


def signin(request):
	if request.method=="POST":
		username=request.POST.get('username',None)
		password=request.POST.get('password',None)
		print(username,password)
		user=authenticate(request,username=username,password=password)
		print(user)
		if user is not None:
			print("Im in")
			login(request,user)
			if username=="admin":
				return redirect("/adminView/")
			else:
				return redirect(f"/feesHistory/{user.id}/")


			

	return render(request,"login.html")

def signup(request):
	if request.method=="POST":
		fullname=request.POST.get('fullname',None)
		email=request.POST.get('email',None)
		username=request.POST.get('username',None)
		password=request.POST.get('password',None)
		grade=request.POST.get('grade',None)
		board=request.POST.get('board',None)
		join_date=request.POST.get('join_date',None)
		
		join_date = datetime.strptime(join_date, "%Y-%m-%d")
		user_exists=User.objects.filter(username=username).exists()
		if not user_exists:
			user=User.objects.create_user(
				username=username,
				password=password,
				email=email,
				first_name=fullname.split()[0],
			
			)
			profile=Profile(
				user=user,
				grade=grade,
				board=board,
				join_date=join_date,
				next_due_date=join_date + timedelta(days=30))
			profile.save()
			login(request,user)
			return redirect("/home/")
		else:
			return HttpResponse("User already exists.Try new Username")
	return render(request,"signup.html")


def about(request):
	return render(request,"about.html")


def feesHistory(request,id):
	user=User.objects.get(id=id)
	all_fees=FeeHistory.objects.filter(user=user)
	return render(request,"feeshistory.html",{'all_fees':all_fees})

def adminView(request):
	users=User.objects.all()
	# if(user.profile.next_due_date-datetime.date.today==timedelta(days=7))

	return render(request,"adminview.html",{'users':users})

def update(request,id):
	student=User.objects.get(id=id)
	# student_fee=FeeHistory.objects.get(id=id)

	if request.method=="POST":
		
		amount=request.POST.get('amount',None)
		paiddate=request.POST.get('paiddate',None)
		student.profile.next_due_date=student.profile.next_due_date+timedelta(days=30)
		student.profile.last_paid=paiddate
		student.profile.save()

		student_fee=FeeHistory(
			user=student,
			paid_date=paiddate,
			amount=amount)
		
		student_fee.save()


	return render(request,"update.html",{'student':student})

def sendmail(request):
	# student=User.objects.all()
	# print(student.profile.next_due_date)
	profiles=Profile.objects.all()
	# for iterator in profiles:
	# 	print(iterator.user)

	users = []
	for profile in profiles:


		if profile.next_due_date is not None:
			diff = profile.next_due_date - timezone.now()
			# print(diff.days)
			if diff.days >=1:
				users.append(profile)
				user = profile.user.email
				print(user)

		
				# send_mail(
				# 'Fee Payment Reminder',
				# 'the due date is coming near.Please make sure you pay it at the earliest.',
				# 'fetoraApp@gmail.com',
				# [user],
				# fail_silently=False,
			 # )
			subject="Fee Payment Reminder"
			message="the due date is coming near.Please make sure you pay it at the earliest."
			to=[user]
			from_email='fetoraApp@gmail.com'


			# message = render_to_string('main/email/email.txt')
			EmailMessage(subject,message,to=to, from_email=from_email).send()


			



	
	# logic for sending emails from emails list
	print(users)
	return HttpResponse("sendmail")