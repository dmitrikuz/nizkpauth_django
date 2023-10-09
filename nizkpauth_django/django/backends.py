from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from nizkpauth.profiles import Profile
from nizkpauth.verifier import Verifier

UserModel = get_user_model()

class NIZKPAuthBackend(ModelBackend):

    def authenticate(self, request, proof):
        username_field = UserModel.USERNAME_FIELD
        lookup_params = {username_field: proof.user_id}

        try:
            user = UserModel.objects.get(**lookup_params)
            user_profile = user.profile
        
        except UserModel.DoesNotExist:
            return None
        
        verifier = Verifier(user_profile)
        if verifier.verify_proof(proof):
            return user
        
        return None

    
