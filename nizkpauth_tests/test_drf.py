from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase
from rest_framework.exceptions import AuthenticationFailed

from nizkpauth.profiles import Profile, ProverProfile
from nizkpauth.prover import Proof, Prover
from nizkpauth.verifier import Verifier
from nizkpauth_django.django.fields import NIZKPProfileField
from nizkpauth_django.drf.authentication import NIZKPAuthentication

TEST_PROFILE_FILEPATH = settings.BASE_DIR / "profiles/test.json"

UserModel = get_user_model()

class TestDjangoNIZKPAuthentication(TestCase):
    def setUp(self):
        user_profile = ProverProfile.load_from_file(TEST_PROFILE_FILEPATH)
        self.user = UserModel.objects.create(
            user_id=user_profile.user_id,
            profile=user_profile.to_public(),
        )
        self.user_proof = Prover(user_profile).create_proof()
        self.auth_header = 'Bearer ' + self.user_proof.to_encoded()
        self.fake_header = 'Bearer ' + self.user_proof.to_encoded().replace('a', 'b')
        self.verifier = Verifier(user_profile.to_public())
        self.factory = RequestFactory()
        self.backend = NIZKPAuthentication()

    def test_auth_view_with_valid_proof(self):
        request = self.factory.get('/any-resource/', HTTP_AUTHORIZATION=self.auth_header)
        user, proof = self.backend.authenticate(request)

        self.assertIsNotNone(user)


    def test_auth_view_with_invalid_proof(self):
        request = self.factory.get('/any-resource/', HTTP_AUTHORIZATION=self.fake_header)
        with self.assertRaises(AuthenticationFailed) as a_failed:
            user, proof = self.backend.authenticate(request)