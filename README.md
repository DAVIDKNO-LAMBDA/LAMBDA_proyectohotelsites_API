# 🏨 LAMBDA Hotel Sites

Sistema hotelero con Django + React

## 🚀 Cómo Probar

### 1. Clonar
```bash
git clone https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API.git
cd LAMBDA_proyectohotelsites_API


Backend (Terminal 1)
cd LAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env


#configurar la db a postgre como esta en el env example 

Frontend (Terminal 2)

cd LAMBDA_proyecto_siteshotel/LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotels
npm install
npm run dev


4. Login
Frontend: http://localhost:3000
Admin: http://localhost:8000/admin
Usuario: El que creaste con createsuperuser
#desde el superusuario hacer un usuario y asignarle el grupo admin para poder hacer login con este 

⚠️ Nota
Proyecto en migración de Power BI - algunos filtros no funcionan completamente.

#la api de los calculos principales estan conectada pero los filtros devuelven los valores del power bi pero ya leen los cvs 



