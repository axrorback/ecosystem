Bu project coderboys.ecosystem uchun maxsus ishlab chiqilmoqda 

Core Team

1.Asadbek To'rayev
2.Ahrorjon Ibrohimjonov

Asosan DRF da Api yozilmoqda 
BackGround ishlar Celery Redis

Container ishlari Docker 

Holat hozir bugung kunda 16/12/2025 holatiga jarayon 20% atrofida bajarildi 


Bugun 19/12/2025

WebSocket Endpoints

1. Task Chat
```postman
ws://domain/ws/tasks/{task_id}/chat/

Auth: JWT (Authorization header)

Send:
{
  "message": "Hello team"
}

Receive:
{
  "user": "ahror",
  "message": "Hello team",
  "created_at": "2025-12-19T21:30:00Z"
}

shunga etibor berilsin Frontend jamoasi 
chunki buni swaggerga qoshib bolmaydi
```


React Misol chat history uchun
```react
const fetchMessages = async (taskId) => {
  const token = localStorage.getItem('access_token');
  const res = await fetch(`/api/chat/tasks/${taskId}/history/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await res.json();
  console.log(data);
};
```
