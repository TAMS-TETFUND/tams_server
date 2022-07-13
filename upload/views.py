import csv

import pandas as pd
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps

import db.models

def model_fields(model_name: str):
    """This method returns the fields in a model"""
    model = apps.get_model(f"db.{model_name}")
    return [field.name for field in model._meta.fields]


def models_open_to_upload():
    """This function returns models that can accept uploads"""
    excluded_models = [
        "LogEntry",
        "Permission",
        "Group",
        "ContentType",
        "Session",
        "AppUser",
        "TokenProxy",
    ]
    models_list = [
        el.__name__
        for el in apps.get_models()
        if el.__name__ not in excluded_models
    ]
    return models_list


def populate_model(request):
    """
    This view will be responsible for populating server models.
    The authorized user will select the model name and upload a csv of
    data to be loaded unto it.
    """
    template = "uploads.html"
    models_list = models_open_to_upload()

    if request.method == "POST":
        selected_model = request.POST["model"]
        if selected_model not in models_list:
            messages.add_message(
                request, messages.ERROR, "Invalid model provided"
            )
            return HttpResponseRedirect(reverse("upload"))

        # checking if uploaded file is a valid csv
        try:
            df = pd.read_csv(request.FILES["data_file"], skipinitialspace=True)
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                f"File Error: {e}",
                extra_tags="text-danger",
            )
            return HttpResponseRedirect(reverse("upload"))

        # check if all the headers in the provided csv are
        # valid model fields.
        selected_model_fields = model_fields(selected_model)
        invalid_cols = [col for col in list(df) if col not in selected_model_fields]
        if len(invalid_cols) != 0:
            messages.add_message(
                request,
                messages.ERROR,
                f"Invalid Column in uploaded file {invalid_cols}.",
                extra_tags="text-danger",
            )
            return HttpResponseRedirect(reverse("upload"))

        # strip whitespaces from df
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        if df.empty:
            messages.add_message(request, messages.WARNING, "File empty")
            return HttpResponseRedirect(reverse("upload"))

        # # remove rows with empty entry for any required column
        # df.dropna(axis=0, inplace=True)

        # remove id column if it exists
        if "id" in df.columns:
            df.drop("id", inplace=True, axis=1)

        failed_rows = []
        # save rows to the model
        for index, row in df.iterrows():
            try:
                eval("db.models.%s" % selected_model).objects.create(**row.to_dict())
            except Exception as e:
                # write failed rows to a list
                failed_rows.append([row.to_dict(), e])
                continue
        if len(failed_rows) > 0:
            context = {"failed_rows": failed_rows, "model": selected_model}
            return render(request, "failed_rows.html", context)
        
        return HttpResponseRedirect(reverse("upload"))

    return render(request, template, {"models": models_list})


def data_file_format(request):
    """
    This view will provide the user with the format of the CSV
    that the server will accept for populating the database.
    """
    template = "upload_format.html"
    models_list = models_open_to_upload()

    if request.method == "POST":
        selected_model = request.POST["model"]
        if selected_model in models_list:
            response = HttpResponse(
                content_type="text/csv",
                headers={
                    "Content-Disposition": 'attachment;filename="%sformat.csv"'
                    % selected_model
                },
            )
            writer = csv.writer(response)
            writer.writerow(model_fields(selected_model))
            return response
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Invalid database table.",
                extra_tags="text-danger",
            )
            return render(request, template, {"models": models_list})
    if request.method == "GET":
        return render(request, template, {"models": models_list})
