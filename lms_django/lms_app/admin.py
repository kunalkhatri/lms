from django.contrib import admin
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

@admin.register(models.classStartTime)
class classStartTimeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.attendance)
class attendanceAdmin(admin.ModelAdmin):

    list_display = ('date','class_start_time','classname','headcount')

    def get_changeform_initial_data(self, request):
        return {'lecturer': request.user}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lecturer" and not request.user.is_superuser :
            kwargs["queryset"] = models.User.objects.filter(id=request.user.id).all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request) :
        if not request.user.is_superuser:
            return super().get_queryset(request).filter(lecturer = request.user)
        return super().get_queryset(request)
    

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('date','class_start_time','classname','headcount','lecturer',)

        return super().get_list_display(request)
    
    def get_list_filter(self, request: HttpRequest):
        if request.user.is_superuser:
            return ('date','classname','class_start_time','lecturer')
        return super().get_list_filter(request)

admin.site.site_header = "Poornima LMS"
admin.site.site_title = "Poornima LMS"
