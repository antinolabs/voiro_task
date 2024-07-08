echo Running tests for user_service...
set PYTHONPATH=C:\Users\Antino\Documents\Voiro_Assignment\voiro_task\user_service
set DJANGO_SETTINGS_MODULE=user_service.settings
pytest --tb=short --disable-warnings user_service/user_service/tests

echo Running tests for profile_service...
set PYTHONPATH=C:\Users\Antino\Documents\Voiro_Assignment\voiro_task\profile_service
set DJANGO_SETTINGS_MODULE=profile_service.settings
pytest --tb=short --disable-warnings profile_service/profile_service/tests

echo Done.
