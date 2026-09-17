from typing import ClassVar  # noqa: EXE002

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from tags.admin import TagsInline

from .forms import BatchImageUploadForm
from .models import Image

THUMB_HEIGHT = 60


def render_thumb(filefield, height=THUMB_HEIGHT):
    if not filefield:
        return "—"
    try:
        url = filefield.url
    except ValueError:
        return "—"
    return format_html(
        '<img src="{}" style="height:{}px;width:auto;border-radius:6px;" />',
        url,
        height,
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_at", "thumb", "tags_list")
    search_fields = ("title",)
    ordering = ("-uploaded_at",)
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"title": ("title",)}
    readonly_fields = ("preview",)
    inlines: ClassVar[list[type[TagsInline]]] = [TagsInline]

    class Media:
        # Chemin relatif au répertoire STATIC (collectstatic/finders)
        js = ("image/image_title_autofill.js",)

    change_list_template = "admin/images/image/change_list.html"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("taggings__tag")  # précharge les tags

    @admin.display(description="Tags")
    def tags_list(self, obj):
        return (
            ", ".join(
                obj.taggings.all()
                .select_related("tag")
                .values_list("tag__label", flat=True)
            )
            or "—"
        )

    @admin.display(description="Aperçu")
    def thumb(self, obj):
        return render_thumb(obj.image_file)

    @admin.display(description="Prévisualisation")
    def preview(self, obj):
        return render_thumb(obj.image_file, height=400)

    # 1) Vue custom — IMPÉRATIF: doit être une méthode d'instance: (self, request)
    def batch_upload_view(self, request):
        opts = self.model._meta
        context = {
            **self.admin_site.each_context(request),
            "opts": opts,
            "title": "Import en lot d’images",
        }

        if request.method == "POST":
            form = BatchImageUploadForm(request.POST, request.FILES)
            context["form"] = form

            if form.is_valid():
                files = form.cleaned_data["files"]  # 👈 déjà une liste
                prefix = form.cleaned_data.get("common_title_prefix", "")

                created = 0
                for f in files:
                    title = f"{prefix}{f.name}" if prefix else f.name
                    self.model.objects.create(title=title, image_file=f)
                    created += 1

                messages.success(
                    request, f"{created} image(s) importée(s) avec succès."
                )
                url = reverse(f"admin:{opts.app_label}_{opts.model_name}_changelist")
                return HttpResponseRedirect(url)
        else:
            context["form"] = BatchImageUploadForm()

        return TemplateResponse(
            request, "admin/images/image/batch_upload.html", context
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "batch-upload/",
                self.admin_site.admin_view(self.batch_upload_view),
                name=f"{self.opts.app_label}_{self.opts.model_name}_batch_upload",
            ),
        ]
        return my_urls + urls
