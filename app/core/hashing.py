import bcrypt

KUTF8 = "utf-8"


class Hasher:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password.

        Args:
            plain_password (str): clear text password
            hashed_password (str): hashed password

        Returns:
            bool: True if the password matches the hashed password
        """
        return bcrypt.checkpw(
            plain_password.encode(KUTF8),
            hashed_password.encode(KUTF8),
        )

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Create a hash of the password.

        Args:
            password (str): clear text password

        Returns:
            str: hashed password
        """
        return bcrypt.hashpw(password.encode(KUTF8), bcrypt.gensalt()).decode(KUTF8)
