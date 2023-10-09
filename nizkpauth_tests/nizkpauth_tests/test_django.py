from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase

from nizkpauth.profiles import Profile, ProverProfile
from nizkpauth.prover import Proof, Prover
from nizkpauth.verifier import Verifier

from nizkpauth_django.django.views import NIZKPBaseAuthView

PROFILE_FILEPATH = f"{settings.BASE_DIR}/profiles/test.json"
UserModel = get_user_model()

class TestDjangoNIZKPAuthentication(TestCase):
    def setUp(self):
        user_profile = ProverProfile.load_from_file(PROFILE_FILEPATH)
        self.user = UserModel.objects.create(
            user_id=user_profile.user_id,
            profile=user_profile.to_public()
        )
        self.user_proof = Prover(user_profile).create_proof()
        self.verifier = Verifier(user_profile.to_public())
        self.factory = RequestFactory()

    def test_auth_view_with_valid_proof(self):
        request = self.factory.post('/login/', data={'proof': self.user_proof.to_encoded()})
        request.session = SessionStore()
        response = NIZKPBaseAuthView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    
    def test_auth_view_with_invalid_proof(self):
        fake_proof = Proof(**vars(self.user_proof))
        fake_proof.challenge = fake_proof.challenge - 24

        request = self.factory.post('/login/', data={'proof': fake_proof.to_encoded()})
        request.session = SessionStore()
        response = NIZKPBaseAuthView.as_view()(request)

        self.assertEqual(response.status_code, 401)