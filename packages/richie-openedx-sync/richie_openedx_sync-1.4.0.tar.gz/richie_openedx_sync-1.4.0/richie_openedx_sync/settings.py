from django.conf import settings

# Load `RICHIE_OPENEDX_SYNC_COURSE_HOOKS` setting using the open edX `ENV_TOKENS` production mode.
settings.RICHIE_OPENEDX_SYNC_COURSE_HOOKS = getattr(settings, "ENV_TOKENS", {}).get(
    "RICHIE_OPENEDX_SYNC_COURSE_HOOKS",
    getattr(settings, "RICHIE_OPENEDX_SYNC_COURSE_HOOKS", []),
)
