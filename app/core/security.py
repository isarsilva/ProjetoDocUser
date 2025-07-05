from passlib.context import CryptContext

password_context = CryptContext( # para criar o contexto de criptografia
    schemes=["bcrypt"], 
    deprecated="auto"
    )

def get_password(password: str) -> str: # para criptografar a senha
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool: # para verificar se a senha é igual a senha criptografada
    return password_context.verify(password, hashed_password)

def verify_passwords(password: str, hashed_password: str) -> bool: 
    return password_context.verify(password, hashed_password)