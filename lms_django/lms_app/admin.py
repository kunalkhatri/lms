from django.contrib import admin, messages
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest

from . import models
# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ('email', 'password', 'is_active')


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','is_active')}),
        (_('Permissions'), {'fields': ( 'is_staff', 'is_superuser','groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(models.className)
class classNameAdmin(admin.ModelAdmin):
    pass

class classStartTimeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        if self.instance.pk is not None:
            # a previous record is being saved, so we let it be
            return cleaned_data
        else:
            # a new record is being added, so we check if there is another record
            if models.classStartTime.objects.all().count() > 0:
                raise ValidationError("You may not add another class Start Time. Max Limit is set to 1.")
            else:
                return cleaned_data


@admin.register(models.classStartTime)
class classStartTimeAdmin(admin.ModelAdmin):
    form = classStartTimeForm
    pass

@admin.register(models.attendance)
class attendanceAdmin(admin.ModelAdmin):

    list_display = ('date','class_start_time','classname','headcount')
    fields = ('lecturer','class_start_time', 'classname', 'date','headcount')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lecturer":
            if request.user.is_superuser or request.user.groups.filter(name = "HODs").exists() :
                return super().formfield_for_foreignkey(db_field, request, **kwargs)
            else:
                kwargs["queryset"] = models.User.objects.filter(id=request.user.id).all()
                kwargs['initial'] = request.user.id
                kwargs['disabled'] = True

        if db_field.name == "class_start_time":
            if request.user.is_superuser or request.user.groups.filter(name = "HODs").exists() :
                return super().formfield_for_foreignkey(db_field, request, **kwargs)
            else:
                kwargs['initial'] = models.classStartTime.objects.first() or None
                kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request) :
        if request.user.is_superuser or request.user.groups.filter(name = "HODs").exists():
            return super().get_queryset(request)
        
        return super().get_queryset(request).filter(lecturer = request.user)
    

    def get_list_display(self, request):
        if request.user.is_superuser or request.user.groups.filter(name = "HODs").exists():
            return ('date','class_start_time','classname','headcount','lecturer',)

        return super().get_list_display(request)
    
    def get_list_filter(self, request: HttpRequest):
        if request.user.is_superuser or request.user.groups.filter(name = "HODs").exists():
            return ('date','classname','class_start_time','lecturer')
        return super().get_list_filter(request)

admin.site.site_header = "Poornima LMS"
admin.site.site_title = "Poornima LMS"
