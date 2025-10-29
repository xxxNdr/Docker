from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

class Login(BaseModel):
    username:str
    password:str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/login')
def api_login(user:Login):
    if user.username == 'admin' and user.password == 'admin':
        return {'success':True, 'message': f"Benvenuto {user.username}"}
    else:
        return{'success':False, 'message':'Dati errati'}

uvicorn.run(app, host='0.0.0.0', port=8000)