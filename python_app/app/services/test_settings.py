from app.services.settings_service import SettingsService

SettingsService.load()

print(SettingsService.get("whisper_model"))

print(SettingsService.get_int("wake_timeout"))

print(SettingsService.get_bool("vad_enabled"))