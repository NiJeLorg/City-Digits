import json
import django
from django.db import transaction
from django.http import HttpResponse, QueryDict
from django.shortcuts import render_to_response
from django.template import RequestContext
import forms
from models import School, Teacher, Team, Student, CityDigitsUser, Interview, Location, InterviewPlayer
from service import MembershipService
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def index(request):
    """
     Loads base index
    """
    current_user = request.user
    return render_to_response('index.html', {},
                              context_instance=RequestContext(request))


@transaction.autocommit
def signUp(request):
    """
      Sign up
    """
    #Process Registration information
    if request.method == 'POST':
        #bound the form
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            #place form data into query dict for easier access
            formData = QueryDict(request.body)
            #create entities
            school = School.objects.create(name=formData.get('schoolName'), address=formData.get('schoolAddress'),
                                           city=formData.get('schoolCity'), state=formData.get('schoolState'))
            teacher = Teacher.objects.create(firstName=formData.get('firstName'), lastName=formData.get('lastName'),
                                             email=formData.get('email'), className=formData.get('className'),
                                             school=school)
            school.save()
            teacher.save()
            #create auth user for teacher
            cityUser = CityDigitsUser(role="TEACHER", username=teacher.email,
                                      password=MembershipService.encryptPassword(teacher.email,
                                                                                 formData.get('password')),
                                      entityId=teacher.id)
            cityUser.save()

            #create teams and students entities
            teamIdx = 0;
            for teamName in formData.getlist('team_name[]'):
                team = Team.objects.create(name=teamName, teacher=teacher)
                team.save()
                #add students to team
                studentIdx = 0;
                for studentName in formData.getlist("student_name[%s][]" % teamIdx):
                    #get password
                    password = MembershipService.encryptPassword(studentName,
                                                                 formData.getlist("student_password[%s][]" % teamIdx)[
                                                                     studentIdx])
                    #get name
                    student = Student.objects.create(firstName=studentName, team=team)
                    student.save()
                    #create auth user for student
                    print "student password: " + password
                    authUser = CityDigitsUser(role="STUDENT", username=student.firstName, password=password,
                                              entityId=student.id)
                    authUser.save()
                    #update index
                    studentIdx = studentIdx + 1

                #updated team index
                teamIdx = teamIdx + 1

            #return response
            json_data = json.dumps({"HTTPRESPONSE": 200})
            return HttpResponse(json_data, mimetype="application/json")
        else:
            #form invalid
            #return and display errors
            return render_to_response('signup.html', {'form': form},
                                      context_instance=RequestContext(request))
        pass
    elif request.method == 'GET':
        #Load Sign up form
        form = forms.SignUpForm()
        return render_to_response('signup.html', {'form': form},
                                  context_instance=RequestContext(request))


def mapNavigation(request):
    """
      Loads the map navigation elements
    """
    return render_to_response('map_navigation.html')


def login(request):
    """
      Handles user login
    """
    if request.method == 'POST':
        #get bound form
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            #attempt to find user username and password
            role = form.cleaned_data["role"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = MembershipService.authenticate(role, username, password)

            #check for authenticated user
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponse(200)
                else:
                    #setup errors to display back to user
                    errors = django.forms.util.ErrorList()
                    errors = form._errors.setdefault(
                        django.forms.forms.NON_FIELD_ERRORS, errors)
                    errors.append('Sorry, this user account is disabled.')
                    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
            else:
                #setup errors
                errors = django.forms.util.ErrorList()
                errors = form._errors.setdefault(
                    django.forms.forms.NON_FIELD_ERRORS, errors)
                errors.append('Username/Password Not Found.')
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))


    elif request.method == 'GET':
        #Load login form
        form = forms.LoginForm()
        return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))


def logout(request):
    """
     Handles user logout
    """
    auth_logout(request)
    return HttpResponse(200)


def interviewSelect(request):
    """
       Interview Select
    """
    return render_to_response('interview_selector.html', context_instance=RequestContext(request))


@transaction.autocommit
def interviewPlayer(request):
    """
      Handles player interview form
    """
    if request.method == "POST":
        #Bound form
        form = forms.PlayerInterviewForm(request.POST, request.FILES)
        if form.is_valid():
            #Save interview related information
            #Get student
            student = MembershipService.findStudentForId(request.user.entityId)
            #Create location
            location = Location(latitude=form.cleaned_data['latitude'], longitude=form.cleaned_data["longitude"],
                                address=form.cleaned_data["location"])
            location.save()
            #Get interview type
            interviewType = request.POST['interview_type']
            #Create player profile
            entity = None
            if interviewType == "PLAYER":
                entity = InterviewPlayer(firstName=form.cleaned_data["firstName"],
                                         do_you_ever_buy_lottery_tickets=form.cleaned_data["buyLotteryTickets"],
                                         why_or_why_not_audio=request.FILES['whyOrWhyNot'],
                                         have_you_ever_won_the_lottery=form.cleaned_data["wonLottery"],
                                         most_won=float(form.cleaned_data["mostWonAmount"]),
                                         money_spent_on_lottery_in_average_week=float(form.cleaned_data["averageSpentOnLotteryPerWeek"]),
                                         jackpot_audio=request.FILES["wonJackpotQuestion"],
                                         photo=request.FILES["photo"])
                entity.save()
            #Create interview
            interview = Interview(student=student, location=location, interviewType=interviewType, entityId=entity.id)
            interview.save()
            return HttpResponse("200")
        else:
            print("FORM ERRORS")
            for e in form.errors:
                print e
            return render_to_response('player_interview.html', {'form': form}, context_instance=RequestContext(request))

    elif request.method == "GET":
        #Load interview form
        form = forms.PlayerInterviewForm()
        #get student team
        team = MembershipService.findStudentForId(request.user.entityId).team.name
        return render_to_response('player_interview.html', {'form': form,'team':team}, context_instance=RequestContext(request))




        #  do_you_ever_buy_lottery_tickets = models.BooleanField()
        # why_or_why_not_audio = models.FilePathField()
        # have_you_ever_won_the_lottery = models.BooleanField()
        # most_won = models.DecimalField
        # money_spent_on_lottery_in_average_week = models.DecimalField
        # jackpot_audio = models.FilePathField()
        # photo = models.FilePathField()