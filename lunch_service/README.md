### lunch_service           
Django project folder.

- Files **'asgi.py'** and **'wsgi.py'** are standard Django files for defining *ASGI* and *WSGI* callables.               
- File **'settings.py'** contains settings information for the project (all installed apps, templates, static and db files directories, default rest_framework settings, etc).         
- File **'urls.py'** contains a list of defined URLs' configurations that routes URLs to the app views:       
  - Path **'admin/'** routes to the standard *Django admin panel*.                   
  - Path **''** (commented) routes to the *app's start webpage*, function *'include'* adds all defined in the *'<app_name>/urls.py'* file URLs.           
  - Path **'api/service-auth/'** routes to the standard *Django Rest Framework (DRF) authentication* page.         
  - Path **'api/service/'** routes to the *Django Rest Framework (DRF) router*, which contains all models viewsets pages (function *'include'* adds all defined in the *'router.urls'* URLs).         
  - Path **'api/service/token/'** routes to the standard *Django Rest Framework (DRF) JWT* tokens receive page.               
  - Path **'api/service/token/refresh/'** routes to the standard *Django Rest Framework (DRF) JWT* access token refresh page.         
  - Path **'api/service/token/verify/'** routes to the standard *Django Rest Framework (DRF) JWT* access token verify page.           
