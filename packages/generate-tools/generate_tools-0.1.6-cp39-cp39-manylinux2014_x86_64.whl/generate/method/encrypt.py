
from requests import post

import generate
from generate.exception import AuthorizedNeeded, GenerateError


class Encrypt:
    def decrypt(
        self: 'generate.Generate',
        string: str
    ) -> str:
        if not self.isAuthorize:
            raise AuthorizedNeeded()
        if not self.authToken:
            raise GenerateError(
                'DecryptError'
                "authorizeToken is required for encrypting string but you don't provide authorizeToken, set your authorizeToken in Generate(..., authorizeToken=authorizeToken, keyword=keyword)"
            )
        if not self.key:
            raise GenerateError(
                'DecryptError'
                "Keyword is required for decrypting string but you don't provide keyword, set your keyword in Generate(..., keyword=keyword)"
            )
        results = post(
            f'{self._apiUrlEncrypt}/api/v1/decrypt',
            json={
                'type': 'ayiin',
                'text': f'{string}',
                'key': self.key
            },
            headers={
                'Content-Type': 'application/json',
                "Authorization": f"Bearer {self.authToken}.{self.key}"
            }
        )
        if results.ok:
            res = results.json()
            return res['result']


    def encrypt(
        self: 'generate.Generate',
        string: str
    ) -> str:
        if not self.isAuthorize:
            raise AuthorizedNeeded()
        if not self.authToken:
            raise GenerateError(
                'EncryptError'
                "authorizeToken is required for encrypting string but you don't provide authorizeToken, set your authorizeToken in Generate(..., authorizeToken=authorizeToken, keyword=keyword)"
            )
        if not self.key:
            raise GenerateError(
                'EncryptError'
                "Keyword is required for encrypting string but you don't provide keyword, set your keyword in Generate(..., authorizeToken=authorizeToken, keyword=keyword)"
            )
        results = post(
            f'{self._apiUrlEncrypt}/api/v1/encrypt',
            json={
                'type': 'ayiin',
                'text': f'{string}',
                'key': self.key
            },
            headers={
                'Content-Type': 'application/json',
                "Authorization": f"Bearer {self.authToken}.{self.key}"
            }
        )
        if results.ok:
            res = results.json()
            return res['result']
