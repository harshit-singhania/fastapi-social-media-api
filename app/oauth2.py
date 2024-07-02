from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt 
from datetime import datetime, timedelta
import schemas 
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# secret key 
SECRET_KEY = '0gstw7zmzymnpbk4xkvorizlmb4vliwl' 
ALGORITHM = 'HS256' 
ACCESS_TOKEN_EXPIRES_MINS = 30 

def create_access_token(data: dict ) : 
    to_encode = data.copy()
    expire  = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINS) 
    to_encode.update({'exp': expire})
    
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token: str, credentials_exception): 
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get('user_id')
        if id is None: 
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError: 
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)): 
       credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not authorize', headers={'WWW-Authenticate':'Bearer'})
       return verify_access_token(token, credentials_exception=credentials_exception) 
   
 
        