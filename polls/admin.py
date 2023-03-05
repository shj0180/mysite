from django.contrib import admin
# models前必须有个点
from .models import Question


# Register your models here.
#
# Make the poll app modifiable in the admin¶
# But where’s our poll app? It’s not displayed on the admin index page.
#
# Only one more thing to do: we need to tell the admin that Question objects have an admin interface.
# To do this, open the polls/admin.py file, and edit it to look like this:
#

admin.site.register(Question)



