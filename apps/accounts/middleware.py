from django.shortcuts import redirect
from django.urls import reverse


class ForceAdminPasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user.is_staff:
            reset_flag = getattr(user, "admin_password_reset_required", None)
            if reset_flag and reset_flag.required:
                allowed_paths = {
                    reverse("admin:password_change"),
                    reverse("admin:password_change_done"),
                    reverse("admin:logout"),
                }
                if request.path.startswith("/admin/") and request.path not in allowed_paths:
                    return redirect("admin:password_change")

        response = self.get_response(request)

        if (
            user.is_authenticated
            and user.is_staff
            and request.path == reverse("admin:password_change_done")
        ):
            reset_flag = getattr(user, "admin_password_reset_required", None)
            if reset_flag and reset_flag.required:
                reset_flag.required = False
                reset_flag.save(update_fields=["required"])

        return response
