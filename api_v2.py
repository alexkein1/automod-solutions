from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserVerificationRequest(BaseModel):
    user_id: int


class UserVerificationResponse(BaseModel):
    status: str
    message: str


@app.post('/verify', response_model=UserVerificationResponse)
def verify_user(request_data: UserVerificationRequest):
    # Здесь можно добавить код для проверки пользователя и генерации ответа
    response_data = {'status': 'success', 'message': f'User {request_data.user_id} verified'}
    return response_data


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
