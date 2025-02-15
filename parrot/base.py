from django.db import models
from django.contrib.auth.models import User

# This file can be used to create shared resources between applications

class BaseModel(models.Model):
    """
    Base model that allows for additional tracking of creation and update of models.
    All application models should inherit from this abstract model instead of models.Model.
    """

    creation_date = models.DateTimeField(
        auto_now_add=True, editable=False, null=True, verbose_name='Creation Date')
    last_update_date = models.DateTimeField(
        auto_now=True, editable=False, null=True, verbose_name='Last Update Date')

    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="+",
        editable=False, db_column="created_by", default=1,
    )
    last_updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="+",
        editable=False, db_column="last_updated_by", default=1
    )

    class Meta:
        abstract = True

    def created_by_name(self):
        if self.created_by:
            return self.created_by.get_full_name().strip() or self.created_by.username

    def last_updated_by_name(self):
        if self.last_updated_by:
            return self.last_updated_by.get_full_name().strip() or self.last_updated_by.username
        