from .resources import LoginResource, RegistrationResource, GetUser1, GetUser2
from app.resources import LoginResource, RegistrationResource, WelcomeResource
from .resources import LoginResource, RegistrationResource, WelcomeResource, AdminLogResource, AdminBanResource  # Add the new imports

def register_routes(api):
    api.add_resource(LoginResource, '/login')
    api.add_resource(RegistrationResource, '/register')
    api.add_resource(GetUser1, '/get1')
    api.add_resource(GetUser2, '/get2')
    api.add_resource(WelcomeResource, '/welcome', endpoint='welcome')
    api.add_resource(AdminLogResource, '/admin/logs')
    api.add_resource(AdminBanResource, '/admin/ban')
    # Add more routes as needed
