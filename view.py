import json
import os
from typing import Tuple, Union

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .forms import ImportForm
from .tests.mock_data import mock_func
from .utils import  get_imported_files_choices
from utils_obj import ConfigClient
User = get_user_model()



class ImportMixin:
    """provide methods to download files(object) from storage using credentials"""

    change_list_template = "configs/admin/change_list.html"
    import_template = "configs/admin/import.html"
    sharing_configs_import_form = ImportForm

    

    def import_from_view(self, request, **kwargs):
        """
        return template with form and process data if form is filled;
        make API call to API point to download an object

        """
        info = (
            self.model._meta.app_label,
            self.model._meta.model_name,
        )
        if request.method == "POST":
            api_response_list_files = []
            if request.headers.get("x-requested-with") == "XMLHttpRequest":                
                # mock an api call to get a list of folders
                data = json.load(request)                
                folder = data.get("folder", None)
                # API call to fetch files for a given folder
                api_response_list_files = get_imported_files_choices(folder)                
                if api_response_list_files:
                    return JsonResponse(
                        {"resp": api_response_list_files, "status_code": 200}
                    )
                else:
                    return JsonResponse({"status_code": 400})

            form = self.get_sharing_configs_import_form(request.POST)
            file_name = form.data.get("file_name")
            form.fields["file_name"].choices = [(file_name, file_name)]

            if form.is_valid():                
                data = {
                    "folder": form.cleaned_data.get("folder"),
                    "filename": form.cleaned_data.get("file_name"),
                }
                               
                # resp = requests.post()
                client = ConfigClient()
                client.import_data(data)

                msg = format_html(
                    _("The object {object} has been imported successfully!"),
                    object=object,
                )
                self.message_user(request, msg, level=messages.SUCCESS)
                return redirect(reverse(f"admin:{info[0]}_{info[1]}_import"))

            else:
                # form is NOT valid
                # print("form NOT valid")
                # print(form["file_name"].field.error_messages["required"]) # This field is required.
                # print(form.errors["file_name"].data) # [ValidationError(['This field is required.'])]
                return render(
                    request,
                    self.import_template,
                    {
                        "form": form,
                        "opts": self.model._meta,
                    },
                )
        else:
            # field folder is pre-filled with resp from API (does not exist yet)
            # current source == json file with data
            form = self.get_sharing_configs_import_form()
            return render(
                request,
                self.import_template,
                {"form": form, "opts": self.model._meta},
            )

    def get_urls(self):
        urls = super().get_urls()
        info = (
            self.model._meta.app_label,
            self.model._meta.model_name,
        )

        my_urls = [
            path(
                f"import/",
                self.admin_site.admin_view(self.import_from_view),
                name="%s_%s_import" % info,
            ),
        ]

        return my_urls + urls

    
