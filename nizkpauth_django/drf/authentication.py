from django.contrib.auth import get_user_model, authenticate
from rest_framework.request import Request
from rest_framework import HTTP_HEADER_ENCODING, authentication
from rest_framework import exceptions

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from nizkpauth.verifier import Verifier
from nizkpauth.prover import Proof
from nizkpauth.utils import decode_string
from nizkpauth.exceptions import InvalidProofFormat

from nizkpauth_django.utils import make_utc

from datetime import datetime


HEADER_NAME = "Bearer"


class NIZKPAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: Request):
        auth = authentication.get_authorization_header(request).split()

        if not auth:
            return None
        
        self.validate_authorization_header(auth)
    
        try:
            proof = Proof.from_encoded(auth[1])
            self._validate_proof(proof)

        except InvalidProofFormat:
            message = _("Proof format is invalid or there is an error in decoding")
            raise exceptions.AuthenticationFailed(message)

        return self.authenticate_proof(request, proof)
    
    
    def authenticate_proof(self, request, proof: Proof):
        user = authenticate(request, proof=proof)

        if user is None:
            raise exceptions.AuthenticationFailed(_('Proof is not valid'))
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted'))
        
        return (user, proof)
    

    def _validate_proof(self, proof):
        now_timestamp = timezone.now()
        proof_timestamp = make_utc(datetime.strptime(proof.other_info, "%H:%M:%S %d/%m/%Y"))
        delta = now_timestamp - proof_timestamp
        seconds_in_minute = 60

        if delta.seconds < 0 or delta.seconds > 60*seconds_in_minute:
            raise InvalidProofFormat



    def validate_authorization_header(self, header):
        if not header or header[0].lower() != HEADER_NAME.lower().encode():
            return None

        if len(header) <= 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        
        elif len(header) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)



    
