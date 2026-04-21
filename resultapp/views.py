from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    notices = Notice.objects.all().order_by('-id')
    return render(request, 'index.html', locals())

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice_detail.html', locals())

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')   
    
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # if  user is not None and user.is_superuser:
        if user is not None:
            login (request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid username or password'

    return render(request, 'admin_login.html', locals())

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    total_students =  Student.objects.count()
    total_subjects =  Subject.objects.count()
    total_classes =  Class.objects.count()
    total_results  =  Result.objects.values('student').distinct().count()
    return render(request, 'admin_dashboard.html', locals())

def admin_logout(request):
    logout(request)
    return redirect('admin-login')

@login_required(login_url='admin-login')
def create_class(request):
    if request.method == 'POST':  
        try:
            class_name = request.POST['classname']
            class_numeric = request.POST['classnumeric']
            class_section = request.POST['section']
            Class.objects.create(class_name=class_name, class_numeric=class_numeric, section=class_section)
            messages.success(request, 'Class created successfully!')
            return redirect('create_class')
        except Exception as e:
            messages.error(request, f'An error occurred while creating the class: {str(e)}')
            return redirect('create_class')
    return render(request, 'create_class.html')


@login_required(login_url='admin-login')
def manage_classes(request):
    classes = Class.objects.all()

    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            Class.objects.filter(id=class_id).delete()
            messages.success(request, 'Class deleted successfully!')
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the class: {str(e)}')
            return redirect('manage_classes')

    return render(request, 'manage_classes.html', locals())


@login_required(login_url='admin-login')
def edit_class(request, class_id):
    class_instance = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        try:    
            class_instance.class_name = request.POST['classname']
            class_instance.class_numeric = request.POST['classnumeric']
            class_instance.section = request.POST['section']
            class_instance.save()
            messages.success(request, 'Class updated successfully!')
            return redirect('manage_classes')
        except Exception as e:
            messages.error(request, f'An error occurred while updating the class: {str(e)}')
            return redirect('edit_class', class_id=class_id)

    return render(request, 'edit_class.html', locals())


@login_required(login_url='admin-login')
def create_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST['subjectname']
            subject_code = request.POST['subjectcode']
            Subject.objects.create(subject_name=subject_name, subject_code=subject_code)
            messages.success(request, 'Subject created successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while creating the subject: {str(e)}')
        return redirect('create_subject')
    return render(request, 'create_subject.html')

@login_required(login_url='admin-login')
def manage_subject(request):
    subjects = Subject.objects.all()

    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            Subject.objects.filter(id=subject_id).delete()
            messages.success(request, 'Subject deleted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the subject: {str(e)}')
        return redirect('manage_subject')

    return render(request, 'manage_subject.html', locals())


@login_required(login_url='admin-login')
def edit_subject(request, subject_id):
    subject_instance = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        try:
            subject_instance.subject_name = request.POST['subjectname']
            subject_instance.subject_code = request.POST['subjectcode']
            subject_instance.save()
            messages.success(request, 'Subject updated successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while updating the subject: {str(e)}')
        return redirect('manage_subject')
    return render(request, 'edit_subject.html', locals())


@login_required(login_url='admin-login')
def add_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            class_id = request.POST['class']
            subject_id = request.POST['subject']
            SubjectCombination.objects.create(student_class_id=class_id, subject_id=subject_id, status=1)
            messages.success(request, 'Subject combination added successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while adding the subject combination: {str(e)}')
        return redirect('add_subject_combination')
    return render(request, 'add_subject_combination.html', locals())


@login_required(login_url='admin-login')
def manage_subject_combination(request):
    subject_combinations = SubjectCombination.objects.all()
    aid = request.GET.get('aid')
    if request.GET.get('aid'):
        try:
            SubjectCombination.objects.filter(id=aid).update(status=1 )
            messages.success(request, 'Subject combination activated successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('manage_subject_combination')

    did = request.GET.get('did')
    if request.GET.get('did'):
        try:
            SubjectCombination.objects.filter(id=did).update(status=0)
            messages.success(request, 'Subject combination deactivated successfully!')
        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}')
        return redirect('manage_subject_combination')

    return render(request, 'manage_subject_combination.html', locals())


@login_required(login_url='admin-login')
def add_student(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            roll_number = request.POST['rollnumber']
            email_id = request.POST['emailid']
            gender = request.POST['gender']
            dob = request.POST['dob']
            class_id = request.POST['class']

            Student.objects.create(
                student_class_id=class_id,
                first_name=first_name,
                last_name=last_name,
                roll_number=roll_number,
                email=email_id,
                gender=gender,
                dob=dob
            )
            messages.success(request, 'Student added successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while adding the student: {str(e)}')
        return redirect('add_student')
    return render(request, 'add_student.html', locals())



@login_required(login_url='admin-login')
def manage_students(request):
    students = Student.objects.all()
    
    return render(request, 'manage_students.html', locals())


@login_required(login_url='admin-login')
def edit_student(request, student_id):
    student_instance = get_object_or_404(Student, id=student_id)
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            student_instance.first_name = request.POST['firstname']
            student_instance.last_name = request.POST['lastname']
            student_instance.roll_number = request.POST['rollnumber']
            student_instance.email = request.POST['emailid']
            student_instance.gender = request.POST['gender']
            student_instance.dob = request.POST['dob']
            student_instance.status = request.POST['status']    
            student_instance.save()

            messages.success(request, 'Student updated successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while updating the student: {str(e)}')
        return redirect('manage_students')
    return render(request, 'edit_student.html', locals())


@login_required(login_url='admin-login')
def add_notice(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            detail = request.POST['details']

            Notice.objects.create(notice_title=title,notice_detail=detail)
            messages.success(request, 'Notice added successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while adding the notice: {str(e)}')
        return redirect('add_notice')
    return render(request, 'add_notice.html', locals())



@login_required(login_url='admin-login')
def manage_notice(request):
    notices = Notice.objects.all()

    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            Notice.objects.filter(id=notice_id).delete()
            messages.success(request, 'Notice deleted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while deleting the notice: {str(e)}')
        return redirect('manage_notice')

    return render(request, 'manage_notice.html', locals())    




@login_required(login_url='admin-login')
def add_result(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class')
            student_id = request.POST.get('studentid')

            # ✅ Get subjects for selected class
            subject_combinations = SubjectCombination.objects.filter(
                student_class_id=class_id,
                status=1,
                subject__isnull=False   # ✅ avoid null error
            ).select_related('subject')

             # ✅ Loop through subjects and save marks
            for sc in subject_combinations:
                subject = sc.subject

                marks = request.POST.get(f'marks_{subject.id}')

                if marks:  # ✅ only save if marks entered
                    Result.objects.create(
                        student_id=student_id,
                        student_class_id=class_id,   
                        subject_id=subject.id,
                        marks_obtained=marks
                    )

            messages.success(request, 'Result info added successfully!')
            return redirect('add_result')
        except Exception as e:
            messages.error(request, f'Error while adding result: {str(e)}')
        return redirect('add_result')
    return render(request, 'add_result.html', locals())

from django.http import JsonResponse
def get_students_subjects(request):
    class_id = request.GET.get('class_id')

    if class_id:
        students = list(Student.objects.filter(student_class_id=class_id)
        .values('id','first_name','last_name','roll_number'))
        
        subject_combinations = SubjectCombination.objects.filter(student_class_id=class_id,status=1,subject__isnull=False).select_related('subject')

        subjects = [{'id': sc.subject.id, 'name':sc.subject.subject_name}for sc in subject_combinations if sc.subject]
        return JsonResponse({'students':students, 'subjects':subjects})
    return JsonResponse({'students':[], 'subjects':[]})


@login_required(login_url='admin-login')
def manage_result(request):
    results = Result.objects.select_related('student','student_class').all()
    students = {}
    for res in results:
        stu_id = res.student.id
        if stu_id not in students:
            students[stu_id] = {
                'student': res.student,
                'class': res.student_class,
                'reg_date': res.student.reg_date,
                'status': res.student.status,               
            }

    return render(request, 'manage_result.html', {'results': students.values()})


@login_required(login_url='admin-login')
def edit_result(request, stdid):
    student = get_object_or_404(Student, id=stdid)
    results = Result.objects.filter(student=student)
    if request.method == 'POST':
        ids = request.POST.getlist('id[]')
        marks = request.POST.getlist('marks[]')

        for i in range(len(ids)):
            result_obj = Result.objects.get(id=ids[i])
            result_obj.marks_obtained = marks[i]
            result_obj.save()
        messages.success(request, 'Result updated successfully')
        return redirect('manage_result')
    return render(request, 'edit_result.html', locals())


from django.contrib.auth import update_session_auth_hash, authenticate

@login_required(login_url='admin-login')
def change_password(request):

    if request.method == 'POST':
        old = request.POST['old_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if new != confirm:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')

        if old == new:
            messages.error(request, 'New password cannot be same as old password')
            return redirect('change_password')

        user = authenticate(username=request.user.username, password=old)

        if user:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully')
        else:
            messages.error(request, 'Old password is incorrect')
        return redirect('change_password')
    return render(request, 'change_password.html')


def search_result(request):
    classes = Class.objects.all()
    return render(request, 'search_result.html', locals())


def check_result(request):
    if request.method == 'POST':
        roll_num = request.POST['rollnumber']
        class_id = request.POST['class']

        try:
            student = Student.objects.get(roll_number = roll_num, student_class_id = class_id)
            results = Result.objects.filter(student=student)

            total_marks = sum([r.marks_obtained for r in results])
            subject_count = results.count()
            max_marks = subject_count * 100

            percentage = (total_marks / max_marks) * 100 if max_marks > 0 else 0
            percentage = round(percentage,2)
            return render(request, 'result_page.html', locals())
        except Exception as e:
            messages.error(request, f'No result found for given roll number and class. {str(e)}')
        return redirect('search_result')