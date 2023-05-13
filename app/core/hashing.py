import bcrypt


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
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Create a hash of the password.

        Args:
            password (str): clear text password

        Returns:
            str: hashed password
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
