from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views import View

from nizkpauth.exceptions import InvalidProofFormat
from nizkpauth.prover import Proof
from nizkpauth_django.utils import validate_proof


class NIZKPBaseAuthView(View):
    def post(self, request, *args, **kwargs):
        
        proof_data = request.POST.get('proof', None)
        if proof_data is not None:
            try:
                proof = Proof.from_encoded(proof_data)
                validate_proof(proof)

            except InvalidProofFormat as e:
                return HttpResponse("Authentication failed", status=401)
            
            user = authenticate(request, proof=proof)

            if user is not None:
                login(request, user)
                return HttpResponse("Success", status=200)
            else:
                return HttpResponse("Authentication failed", status=401)
            
        return HttpResponse("Proof was not provided", status=401)