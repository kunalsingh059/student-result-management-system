from django.db import models

class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_numeric = models.IntegerField()
    section = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.class_name} - {self.section}"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - {self.subject_code}"


class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    ) 

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    roll_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SubjectCombination(models.Model):
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_class} - {self.subject}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    marks_obtained = models.IntegerField()
    posting_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.subject} : {self.marks_obtained}"


class Notice(models.Model):
    notice_title = models.CharField(max_length=200)
    notice_detail = models.TextField()
    posting_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.notice_title}"