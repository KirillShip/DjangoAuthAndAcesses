from django.db import models
import uuid

class Role(models.Model):
    role_name = models.CharField(max_length=100)

class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=255)
    user_email = models.EmailField(null=False)
    role_id = models.ForeignKey(Role, on_delete = models.DO_NOTHING, null=False, default=4, db_column='role_id')
    is_active = models.BooleanField(default=True)

class Element(models.Model):
    element_name = models.CharField(max_length=100)

class Permission(models.Model):
    role_id = models.ForeignKey(Role, on_delete = models.DO_NOTHING, null=False, db_column='role_id')
    element_id = models.ForeignKey(Element, on_delete = models.DO_NOTHING, null=False, db_column='element_id')
    read_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)

class Session(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    user_id = models.ForeignKey(User, on_delete = models.DO_NOTHING, null=False, db_column='user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
