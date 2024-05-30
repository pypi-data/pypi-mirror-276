
from requests import post

import generate
from generate.exception import AuthorizedNeeded, GenerateError


class Encrypt:
    def decrypt(
        self: 'generate.Generate',
        string: str,
        keyword: str = None
    ) -> str:
        """(method) def decrypt(string: str, keyword: str = None) -> str:

        Args:
            string (`str`): Teks Enkripsi untuk di dekripsi.
            keyword (`str`, `optional`): `Kata kunci` untuk menggunakan enkripsi ini. Jika anda tidak mengisikan ini, otomatis `kata kunci` akan menggunakan kata kunci dari `parameter` `class Generate(...)`.


        Raises:
            `AuthorizedNeeded`: Mungkin kamu harus menggunakan `generate.start()` terlebih dahulu.
            `GenerateError`: Kesalahan yang mungkin anda lupa untuk mengisikan `parameter` yang dibutuhkan.

        Returns:
            `str`: Hasil `(method) decrypt(...)` akan mengembalikan string yang didekripsikan
        """
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
        key = keyword if keyword else self.key
        results = post(
            f'{self._apiUrlEncrypt}/api/v1/decrypt',
            json={
                'type': 'ayiin',
                'text': f'{string}',
                'key': key
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
        string: str,
        keyword: str = None
    ) -> str:
        """(method) def encrypt(string: str, keyword: str = None) -> str:

        Args:
            string (`str`): Teks untuk di enkripsi.
            keyword (`str`, `optional`): `Kata kunci` untuk menggunakan enkripsi ini. Jika anda tidak mengisikan ini, otomatis `kata kunci` akan menggunakan kata kunci dari `parameter` `class Generate(...)`.

        Raises:
            `AuthorizedNeeded`: Mungkin kamu harus menggunakan `generate.start()` terlebih dahulu
            `GenerateError`: Kesalahan yang mungkin anda lupa untuk mengisikan `parameter` yang dibutuhkan

        Returns:
            str: hasil `(method) def encrypt(...)` akan mengembalikan string yang dienkripsikan
        """
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
        key = keyword if keyword else self.key
        results = post(
            f'{self._apiUrlEncrypt}/api/v1/encrypt',
            json={
                'type': 'ayiin',
                'text': f'{string}',
                'key': key
            },
            headers={
                'Content-Type': 'application/json',
                "Authorization": f"Bearer {self.authToken}.{self.key}"
            }
        )
        if results.ok:
            res = results.json()
            return res['result']
