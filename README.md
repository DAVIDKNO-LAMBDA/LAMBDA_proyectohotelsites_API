# 🏨 LAMBDA Hotel Sites# 🏨 LAMBDA Hotel Sites - Guía de Inicio Rápido# 🏨 LAMBDA Hotel Sites - Migración Power BI → Web App# 🏨 LAMBDA Hotel Sites Project - Migración Power BI a Web App# 🏨 LAMBDA Hotel Sites Project



Sistema hotelero con Django + React



## 🚀 Cómo ProbarSistema de gestión hotelera con **Django (Backend)** y **React (Frontend)**



### 1. Clonar

```bash

git clone https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API.git⚠️ **PROYECTO EN MIGRACIÓN** - Datos vienen de Power BI, algunos filtros y métricas necesitan ajustes**Sistema hotelero integral** desarrollado con **Django + React + TypeScript**

cd LAMBDA_proyectohotelsites_API

```



### 2. Backend (Terminal 1)---

```bash

cd LAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels

python -m venv venv

venv\Scripts\activate## 🚀 Cómo Probar el Proyecto## ⚠️ ESTADO: MIGRACIÓN ACTIVA DE POWER BISistema de gestión integral para sitios hoteleros desarrollado con Django (Backend) y React (Frontend). Sistema de gestión integral para sitios hoteleros desarrollado con Django (Backend) y React (Frontend). 

pip install -r requirements.txt

cp .env.example .env

```

### 📋 **Requisitos Previos**

Editar `.env`:

```- Python 3.8+

NAME_DATABASE=hoteldb

USER_DATABASE=postgres  - Node.js 18+### ✅ **Completado:**

PASS_DATABASE=123

```- PostgreSQL



```bash- Git- Autenticación JWT + Grupos automáticos

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

```### 1️⃣ **Clonar Repositorio**- Estructura backend/frontend funcional## ⚠️ ESTADO ACTUAL DEL PROYECTO - MIGRACIÓN ACTIVA## ⚠️ ESTADO ACTUAL DEL PROYECTO



### 3. Frontend (Terminal 2)```bash

```bash

cd LAMBDA_proyecto_siteshotel/LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotelsgit clone https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API.git- Carga de datos CSV de Power BI

npm install

npm run devcd LAMBDA_proyectohotelsites_API

```

```- Interface básica de dashboard

### 4. Login

- Frontend: `http://localhost:3000`

- Admin: `http://localhost:8000/admin`

- Usuario: El que creaste con `createsuperuser`### 2️⃣ **Backend (Terminal 1)**



## ⚠️ Nota

Proyecto en migración de Power BI - algunos filtros no funcionan completamente.
#### **Navegar y configurar:**### 🔥 **CRÍTICO - REQUIERE REVISIÓN:****🔄 MIGRACIÓN EN PROCESO**: Este proyecto es una migración activa de dashboards de Power BI a una aplicación web moderna. **� MIGRACIÓN EN PROCESO**: Este proyecto es una migración activa de dashboards de Power BI a una aplicación web moderna. 

```bash

cd LAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels- **Filtros NO funcionan** (frontend → backend)



# Crear entorno virtual- **Métricas incorrectas** vs Power BI original

python -m venv venv

- **Gráficas usan datos falsos** (dummyData.ts)

# Activar (Windows)

venv\Scripts\activate### ✅ Componentes completados:### ✅ Componentes completados:



# Instalar dependencias---

pip install -r requirements.txt

```- ✅ Sistema de autenticación JWT completo- ✅ Sistema de autenticación JWT completo



#### **Configurar base de datos:**## 📁 Ubicaciones Importantes

```bash

# Copiar configuración- ✅ Gestión de usuarios con grupos y permisos automáticos- ✅ Gestión de usuarios con grupos y permisos

cp .env.example .env

```### 🔧 **Backend Django**



**Editar `.env` con tus datos:**```- ✅ Estructura básica de dashboard y componentes React- ✅ Conexión básica de gráficas al backend

```env

SECRET_KEY=tu-clave-secreta-aquiLAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels/

DEBUG=True

FRONTEND_URL=http://localhost:3000├── 📄 manage.py                    # Comando principal- ✅ Carga de datos desde archivos CSV (migrados de Power BI)- ✅ Carga de datos desde archivos CSV (migrados de Power BI)

NAME_DATABASE=hoteldb

USER_DATABASE=postgres├── 📄 requirements.txt             # Dependencias

PASS_DATABASE=tu_password

HOST_DATABASE=localhost├── 📄 .env.example                 # Plantilla configuración- ✅ API endpoints básicos funcionando

PORT_DATABASE=5432

```├── 👤 Usuarios/                    # Autenticación + Grupos



#### **Base de datos PostgreSQL:**│   ├── models.py                   # Usuario personalizado### ⚠️ Componentes en desarrollo:

```sql

-- Abrir PostgreSQL y ejecutar:│   ├── views.py                    # Login/Register JWT

CREATE DATABASE hoteldb;

CREATE USER postgres WITH PASSWORD 'tu_password';│   └── migrations/0002_*.py        # ⭐ Crea grupos automáticos### ⚠️ **PROBLEMAS CRÍTICOS IDENTIFICADOS** - REQUIEREN REVISIÓN:- 🔄 **Filtros dinámicos**: Los filtros del dashboard no están completamente funcionales

GRANT ALL PRIVILEGES ON DATABASE hoteldb TO postgres;

```├── 📊 dashboard/                   # Dashboard + Métricas



#### **Migrar y arrancar:**│   ├── views.py                    # API /api/dashboard/metrics/- 🔄 **Métricas avanzadas**: Cálculos complejos de KPIs en proceso de ajuste

```bash

python manage.py makemigrations│   ├── 🔥 services/metrics_service.py  # ❌ PROBLEMAS AQUÍ

python manage.py migrate

python manage.py runserver│   └── data/                       # CSV de Power BI#### 🔥 **1. Filtros NO Funcionales**- 🔄 **Sincronización de datos**: Algunos datos pueden no reflejar filtros aplicados

```

│       ├── Ventas.csv              # 9,945 registros

✅ **Backend corriendo en:** `http://localhost:8000`

│       ├── Habitaciones.csv        # 18,026 registros- **Ubicación**: `src/contexts/FilterContext.tsx` y `src/components/dashboard/FilterBar.tsx`- 🔄 **Validación de fórmulas**: Las fórmulas de Power BI están siendo adaptadas

### 3️⃣ **Frontend (Terminal 2 - NUEVA TERMINAL)**

│       ├── Huespedes.csv           # Info huéspedes

```bash

cd LAMBDA_proyecto_siteshotel/LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotels│       ├── Forecast.csv            # Proyecciones- **Problema**: Los filtros del frontend NO se aplican correctamente al backend



# Instalar dependencias│       ├── Expensas.csv            # Gastos

npm install

│       ├── Presupuesto.csv         # Presupuestos- **Archivo backend**: `dashboard/services/metrics_service.py` línea 48## �📁 Estructura del Proyecto

# Copiar configuración

cp .env.example .env│       ├── Indicadoresppto.csv     # KPIs objetivo



# Arrancar servidor│       └── Propiedades.csv         # Sites + FARA- **Causa**: La función `calculate_metrics(property_, concept, period)` NO usa los parámetros recibidos

npm run dev

```└── LAMBDA_backend_sites_hotels/



✅ **Frontend corriendo en:** `http://localhost:3000`    ├── settings.py                 # Configuración- **Resultado**: Siempre devuelve datos de TODAS las propiedades sin filtrar```



---    └── urls.py                     # URLs principales



## 👤 Crear Usuario para Login```LAMBDA_proyectohotelsites_API/



### **Opción 1: Superusuario (Recomendado)**



**En Terminal 1 (backend):**### 🎨 **Frontend React**#### 🔥 **2. Cálculos de Métricas Incorrectos**├── LAMBDA_proyecto_siteshotel/

```bash

python manage.py createsuperuser```

```

LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotels/src/- **Ubicación**: `dashboard/services/metrics_service.py` líneas 60-150│   ├── LAMBDA_backend_sites_hotels/         # Backend Django

**Llenar datos:**

```├── 📄 App.tsx                      # Componente principal

Email: admin@lambda.com

Username: admin├── contexts/- **Problema**: Fórmulas migradas de Power BI no coinciden con resultados esperados│   │   ├── Base/                            # App base del sistema

Password: admin123

Password (again): admin123│   ├── AuthContext.tsx             # JWT automático

```

│   └── 🔥 FilterContext.tsx        # ❌ Filtros no aplicados- **Métricas afectadas**:│   │   ├── dashboard/                       # Dashboard y métricas hoteleras

### **Opción 2: Usuario desde Admin Web**

├── hooks/

1. **Ir a:** `http://localhost:8000/admin`

2. **Login** con el superusuario creado arriba│   └── 🔥 useDashboardData.ts      # ❌ Hook datos dashboard  - % Ocupación (línea 60-64)│   │   │   ├── data/                        # Datos CSV migrados de Power BI

3. **Click en "Usuarios"** → **"Agregar Usuario"**

4. **Llenar:**├── lib/

   - Email: `usuario@lambda.com`

   - Username: `usuario`│   ├── api.ts                      # Cliente HTTP + JWT  - ADR - Average Daily Rate (línea 74-77)│   │   │   │   ├── Ventas.csv              # Datos de ventas por fecha/propiedad

   - Password: `usuario123`

5. **Guardar y continuar editando**│   └── 🔥 dummyData.ts             # ❌ DATOS FALSOS

6. **Marcar:**

   - ✅ Active├── components/dashboard/  - RevPAR - Revenue per Available Room (línea 78-80)│   │   │   │   ├── Habitaciones.csv        # Ocupación de habitaciones

   - ✅ Staff status (para acceso admin)

   - ✅ Estado del usuario│   ├── 🔥 FilterBar.tsx            # ❌ NO conectado backend

7. **En sección "Groups"** → Agregar grupo:

   - **Admin** (acceso completo)│   ├── KPICard.tsx                 # Métricas display  - Cumplimiento vs Presupuesto (línea 65-73)│   │   │   │   ├── Huespedes.csv           # Información de huéspedes

   - **Inversionista** (solo lectura)

8. **Guardar**│   ├── LineChart.tsx               # Gráfica líneas



---│   ├── BarChart.tsx                # Gráfica barras│   │   │   │   ├── Forecast.csv            # Proyecciones (RevPAR, ADR, etc.)



## 🌐 Probar la Aplicación│   └── PieChart.tsx                # Gráfica circular



### **1. Login Frontend**└── pages/#### 🔥 **3. Datos de Gráficas Hardcodeados**│   │   │   │   ├── Expensas.csv            # Gastos operativos

1. **Ir a:** `http://localhost:3000`

2. **Usar credenciales:**    ├── Login.tsx                   # Autenticación

   - Email: `admin@lambda.com`

   - Password: `admin123`    ├── 🏠 Dashboard.tsx            # Dashboard principal- **Ubicación**: `src/lib/dummyData.ts`│   │   │   │   ├── Presupuesto.csv         # Presupuestos por periodo



### **2. Navegación**    ├── Ventas.tsx                  # Página ventas

- **Dashboard:** Métricas principales (KPIs, gráficas)

- **Ventas:** Página de ventas    ├── Costos.tsx                  # Página costos- **Problema**: Las gráficas usan datos falsos, NO datos reales del backend│   │   │   │   ├── Indicadoresppto.csv     # KPIs presupuestados

- **Costos:** Página de costos  

- **Finanzas:** Página financiera    ├── Finanzas.tsx                # Página finanzas

- **Reportes:** Reportes del sistema

- **Usuarios:** Gestión de usuarios (solo Admin)    ├── Reportes.tsx                # Reportes- **Archivos afectados**: Todos los componentes en `src/components/dashboard/`│   │   │   │   └── Propiedades.csv         # Catálogo de propiedades



### **3. Admin Backend**    └── Usuarios.tsx                # Gestión usuarios

- **Ir a:** `http://localhost:8000/admin`

- **Login** con superusuario```- **Resultado**: Dashboards muestran datos de prueba, no datos reales│   │   │   └── services/                    # Lógica de cálculo de métricas

- **Gestionar:** Usuarios, grupos, permisos



---

---│   │   ├── Usuarios/                        # Gestión de usuarios y permisos

## ⚠️ Problemas Conocidos



### **Filtros No Funcionan**

- Los filtros del dashboard (propiedad, periodo) NO se aplican## 🚀 Instalación Rápida## 📁 Estructura Detallada del Proyecto│   │   │   └── migrations/                  # Incluye creación automática de grupos

- Siempre muestra datos de todas las propiedades

- **Archivo:** `dashboard/services/metrics_service.py`



### **Gráficas con Datos Falsos**### 1️⃣ **Clonar & Backend**│   │   ├── manage.py

- Las gráficas usan datos de prueba

- NO están conectadas al backend real```bash

- **Archivo:** `src/lib/dummyData.ts`

git clone https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API.git```│   │   ├── requirements.txt

### **Métricas vs Power BI**

- Algunos cálculos pueden diferir del Power BI originalcd LAMBDA_proyectohotelsites_API/LAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels

- Requiere validación de fórmulas

LAMBDA_proyectohotelsites_API/│   │   └── .env.example

---

# Python + Django

## 📁 Estructura Básica

python -m venv venv├── 📄 README.md                                    # Este archivo│   └── LAMBDA_front_sites_hotels/           # Frontend React + TypeScript

```

LAMBDA_proyectohotelsites_API/venv\Scripts\activate              # Windows

├── LAMBDA_proyecto_siteshotel/

│   ├── LAMBDA_backend_sites_hotels/     # Django Backendpip install -r requirements.txt├── 📄 .gitignore                                   # Git ignore principal│       └── LAMBDA_front_sites_hotels/       # Aplicación React

│   │   ├── manage.py                    # Comando principal

│   │   ├── dashboard/                   # App dashboard

│   │   │   └── data/                    # Datos CSV de Power BI

│   │   └── Usuarios/                    # App usuarios# Configurar .env├── 📄 .env.example                                 # Variables de entorno raíz│           ├── src/

│   └── LAMBDA_front_sites_hotels/       # React Frontend

│       └── LAMBDA_front_sites_hotels/cp .env.example .env

│           ├── src/                     # Código fuente

│           └── package.json# Editar: SECRET_KEY, DB, EMAIL└── LAMBDA_proyecto_siteshotel/│           │   ├── components/dashboard/    # Componentes de gráficas

```

```

---

    ├── 🔧 LAMBDA_backend_sites_hotels/              # *** BACKEND DJANGO ***│           │   ├── pages/                   # Páginas del sistema

## 🛠️ Comandos Útiles

### 2️⃣ **Base de Datos**

### **Backend**

```bash```sql    │   ├── 📄 manage.py                             # Comando principal Django│           │   ├── contexts/                # Estado global y autenticación

# Ver logs de desarrollo

python manage.py runserver-- PostgreSQL



# Crear nuevo superusuarioCREATE DATABASE hoteldb_lambda;    │   ├── 📄 requirements.txt                      # Dependencias Python│           │   └── lib/api.ts              # Cliente HTTP con JWT

python manage.py createsuperuser

CREATE USER tu_usuario WITH PASSWORD 'tu_password';

# Aplicar cambios DB

python manage.py makemigrationsGRANT ALL PRIVILEGES ON DATABASE hoteldb_lambda TO tu_usuario;    │   ├── 📄 .env                                  # Variables entorno (NO subir)│           ├── package.json

python manage.py migrate

``````



### **Frontend**      │   ├── 📄 .env.example                          # Plantilla variables entorno│           └── .env.example

```bash

# Desarrollo```bash

npm run dev

# Django    │   ├── ├── .gitignore

# Build producción

npm run buildpython manage.py makemigrations

```

python manage.py migrate          # ⭐ Crea grupos Admin/Inversionista    │   ├── 👤 Usuarios/                             # *** APP USUARIOS ***└── README.md

---

python manage.py createsuperuser  # Email: admin@lambda.com

## 📞 Información

python manage.py runserver        # → http://localhost:8000    │   │   ├── 📄 models.py                         # Modelo Usuario personalizado```

- **Repositorio:** [LAMBDA_proyectohotelsites_API](https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API)

- **Stack:** Django + React + TypeScript + PostgreSQL```

- **Estado:** Migración activa de Power BI a Web App

    │   │   ├── 📄 views.py                          # Login/Register/Refresh JWT

---

### 3️⃣ **Frontend**

⚡ **¿Problemas?** Revisar que ambos servidores estén corriendo y PostgreSQL configurado correctamente.
```bash    │   │   ├── 📄 urls.py                           # Rutas: /api/usuarios/## 🚀 Guía de Instalación Completa

# Nueva terminal

cd LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotels    │   │   ├── 📄 serializers.py                    # Serializadores JWT

npm install

cp .env.example .env              # VITE_API_URL=http://localhost:8000/api    │   │   ├── 📄 backends.py                       # Autenticación personalizada### Prerrequisitos

npm run dev                       # → http://localhost:3000

```    │   │   └── migrations/



---    │   │       ├── 0001_initial.py                  # Migración modelo Usuario- Python 3.8+



## 👥 Gestión de Usuarios    │   │       └── 0002_asignar_permisos_grupos.py  # ⭐ CREA GRUPOS AUTOMÁTICOS- Node.js 18+



### **Admin Django:** `http://localhost:8000/admin`    │   │- PostgreSQL 12+



1. **Login** con superusuario    │   ├── 📊 dashboard/                            # *** APP DASHBOARD ***- Git

2. **Usuarios → Agregar Usuario**

3. **Completar:**    │   │   ├── 📄 views.py                          # API endpoint /api/dashboard/metrics/

   - Email: `usuario@lambda.com`

   - Username: `usuario_lambda`      │   │   ├── 📄 urls.py                           # Rutas dashboard### 1. Clonar el Repositorio

   - Password: `password123`

4. **Configurar permisos:**    │   │   ├── 📁 data/                            # *** DATOS CSV DE POWER BI ***

   - ✅ Active + Staff status

   - ✅ Estado del usuario    │   │   │   ├── 💰 Ventas.csv                   # Datos ventas por fecha/propiedad```bash

5. **Asignar grupo:**

   - **Admin**: Permisos completos    │   │   │   ├── 🏨 Habitaciones.csv             # Ocupación habitacionesgit clone https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API.git

   - **Inversionista**: Solo lectura

6. **Guardar** → Verificar login en frontend    │   │   │   ├── 👥 Huespedes.csv                # Info huéspedes  cd LAMBDA_proyectohotelsites_API



### **Grupos Automáticos:**    │   │   │   ├── 📈 Forecast.csv                 # Proyecciones RevPAR/ADR```

- **Admin** → `change_*`, `add_*`, `delete_*`, `view_*`

- **Inversionista** → Solo `view_*`    │   │   │   ├── 💸 Expensas.csv                 # Gastos operativos



---    │   │   │   ├── 📋 Presupuesto.csv              # Presupuestos por periodo### 2. Configuración del Backend (Django)



## 🔥 PROBLEMAS CRÍTICOS IDENTIFICADOS    │   │   │   ├── 📊 Indicadoresppto.csv          # KPIs presupuestados



### ❌ **1. Filtros No Funcionan**    │   │   │   └── 🏢 Propiedades.csv              # Catálogo propiedades + FARA```bash



**Ubicación:** `dashboard/services/metrics_service.py:48`    │   │   └── services/# Navegar al directorio del backend



```python    │   │       └── 🔥 metrics_service.py           # *** AQUÍ ESTÁN LOS PROBLEMAS ***cd LAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels

def calculate_metrics(property_: str, concept: str, period: str):

    # ❌ PROBLEMA: Parámetros NO se usan    │   │

    ventas = d["ventas"]  # Siempre TODOS los datos

        │   ├── 🏢 Base/                                 # App base del sistema# Crear entorno virtual

    # ✅ DEBERÍA SER:

    # if property_ != "all":    │   └── LAMBDA_backend_sites_hotels/             # Configuración Djangopython -m venv venv

    #     ventas = ventas.query("Propiedad == @property_")

    #     habitaciones = habitaciones.query("Propiedad == @property_")    │       ├── 📄 settings.py                       # Configuración principal

```

    │       ├── 📄 urls.py                          # URLs principales del proyecto# Activar entorno virtual (Windows)

**Frontend envía:** `property="sites45"` pero backend ignora

    │       └── 📄 wsgi.py                          # Configuración WSGIvenv\Scripts\activate

### ❌ **2. Gráficas Datos Falsos**

    │# En macOS/Linux: source venv/bin/activate

**Ubicación:** `src/lib/dummyData.ts`

    └── 🎨 LAMBDA_front_sites_hotels/               # *** FRONTEND REACT ***

```tsx

// En Dashboard.tsx líneas 24-30        └── LAMBDA_front_sites_hotels/               # Aplicación React# Instalar dependencias

import { salesTrendData } from "@/lib/dummyData";  // ❌ FALSO

// ✅ DEBE conectar a API real            ├── 📄 package.json                      # Dependencias Node.jspip install -r requirements.txt

```

            ├── 📄 vite.config.ts                    # Configuración Vite

### ❌ **3. Métricas vs Power BI**

            ├── 📄 .env.example                      # Variables entorno frontend# Configurar variables de entorno

**Archivo:** `dashboard/services/metrics_service.py:60-150`

            └── src/cp .env.example .env

**Revisar fórmulas:**

- **% Ocupación** (línea 60): Query habitaciones                ├── 📄 App.tsx                       # Componente principal```

- **ADR** (línea 74): `ventas_alojamiento / hab_ocupadas`

- **RevPAR** (línea 78): `ventas_alojamiento / hab_totales`                ├── 📄 main.tsx                      # Punto entrada React



---                ├── #### 📝 Editar .env con tus configuraciones:



## 📊 Datos Power BI                ├── 📁 contexts/                     # *** CONTEXTOS GLOBALES ***



### **CSV Migrados** (`dashboard/data/`)                │   ├── 🔐 AuthContext.tsx           # Manejo autenticación JWT```env



| Archivo | Registros | Contenido | Formato |                │   └── 🔥 FilterContext.tsx         # ⚠️ FILTROS NO FUNCIONANSECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria

|---------|-----------|-----------|---------|

| **Ventas.csv** | 9,945 | Ingresos por fecha/propiedad | `Titulo\|Valor\|Fecha\|Propiedad` |                │DEBUG=True

| **Habitaciones.csv** | 18,026 | Ocupación habitaciones | `Subconcepto\|General\|Valor` |

| **Huespedes.csv** | - | Número huéspedes | Para tarifa promedio |                ├── 📁 hooks/                        # *** HOOKS PERSONALIZADOS ***FRONTEND_URL=http://localhost:3000

| **Forecast.csv** | - | RevPAR/ADR proyectado | Comparar real vs forecast |

| **Propiedades.csv** | 5 | Sites + Factor FARA | Sites 45, BAQ, MDE, CTG, SMR |                │   └── 🔥 useDashboardData.ts       # ⚠️ Hook datos dashboardNAME_DATABASE=hoteldb_lambda



**Separador:** `|` (pipe) • **Encoding:** `latin1`                │USER_DATABASE=postgres



---                ├── 📁 lib/                          # *** UTILIDADES ***PASS_DATABASE=tu_password



## 🔧 APIs Disponibles                │   ├── 🌐 api.ts                    # Cliente HTTP + JWT automáticoHOST_DATABASE=localhost



### **Autenticación**                │   ├── 🔥 dummyData.ts              # ⚠️ DATOS FALSOS EN GRÁFICASPORT_DATABASE=5432

```

POST /api/usuarios/login/     # Email + Password → JWT                │   └── 📄 utils.ts                  # Utilidades generalesEMAIL_HOST_USER=tu_email@gmail.com

POST /api/usuarios/refresh/   # Renovar token

GET  /api/usuarios/profile/   # Info usuario                │EMAIL_HOST_PASSWORD=tu_app_password_gmail

```

                ├── 📁 components/                   # *** COMPONENTES UI ***```

### **Dashboard**

```                │   ├── dashboard/                   # Componentes dashboard

GET /api/dashboard/metrics/   # Filtros NO funcionan

    ?property=sites45         # Ignorado                │   │   ├── 🔥 FilterBar.tsx         #  Filtros no aplicados#### 🗃️ Configurar base de datos PostgreSQL:

    &concept=alojamiento     # Ignorado  

    &period=month            # Ignorado                │   │   ├── 📊 KPICard.tsx           # Tarjetas métricas

```

                │   │   ├── 📈 LineChart.tsx         # Gráfica líneas```sql

---

                │   │   ├── 📊 BarChart.tsx          # Gráfica barras  -- Conectar a PostgreSQL como superusuario

## 🛠️ Tareas Pendientes

                │   │   └── 🥧 PieChart.tsx          # Gráfica circularCREATE DATABASE hoteldb_lambda;

### 🔥 **CRÍTICO**

- [ ] **Implementar filtros** en `metrics_service.py`                │   ├── layout/                      # Layout aplicaciónCREATE USER tu_usuario WITH PASSWORD 'tu_password';

- [ ] **Conectar gráficas** a datos reales (eliminar dummyData)

- [ ] **Validar métricas** vs Power BI original                │   └── ui/                          # Componentes base (shadcn/ui)GRANT ALL PRIVILEGES ON DATABASE hoteldb_lambda TO tu_usuario;



### 📋 **ALTO**                │```

- [ ] Cache datos CSV (se cargan cada request)

- [ ] Loading states + manejo errores                └── 📁 pages/                        # *** PÁGINAS PRINCIPALES ***

- [ ] Endpoints específicos para gráficas

                    ├── 🔐 Login.tsx                 # Página login#### 🔄 Ejecutar migraciones:

### 📊 **MEDIO**

- [ ] Export reportes                    ├── 🏠 Dashboard.tsx             # ⭐ Dashboard principal

- [ ] Dashboards por rol

- [ ] Notificaciones                    ├── 💰 Ventas.tsx                # Página ventas```bash



---                    ├── 💸 Costos.tsx                # Página costos# Crear y aplicar migraciones



## 🚢 Comandos Útiles                    ├── 📊 Finanzas.tsx              # Página finanzaspython manage.py makemigrations



### **Backend Debug**                    ├── 📋 Reportes.tsx              # Página reportespython manage.py migrate

```bash

python manage.py shell                    ├── 👥 Usuarios.tsx              # Gestión usuarios```

>>> from dashboard.services.metrics_service import calculate_metrics

>>> result = calculate_metrics("sites45", "alojamiento", "month")                    └── 📧 Boletin.tsx               # Boletín informativo

>>> print(result)  # Verificar si aplica filtros

``````**✅ Esto creará automáticamente los grupos:**



### **Frontend**- `Admin` - Permisos completos

```bash

npm run dev          # Desarrollo## 🚀 Guía de Instalación Completa- `Inversionista` - Solo lectura

npm run build        # Producción

npm run preview      # Preview build

```

### Prerrequisitos#### 👤 Crear superusuario:

---



## 📋 Checklist Estado

- Python 3.8+```bash

### ✅ **Funcional**

- [x] Autenticación JWT + renovación automática- Node.js 18+python manage.py createsuperuser

- [x] Grupos y permisos (Admin/Inversionista)

- [x] Estructura básica frontend/backend- PostgreSQL 12+```

- [x] Carga datos CSV Power BI

- Git

### ⚠️ **Requiere Atención**

- [ ] 🔥 **Filtros funcionales** (Crítico)Proporciona:

- [ ] 🔥 **Métricas precisas** (Crítico)

- [ ] 🔥 **Datos reales en gráficas** (Crítico)### 1. Clonar el Repositorio- **Email**: admin@lambda.com (o tu email preferido)

- [ ] Performance optimización

- [ ] Validación completa vs Power BI- **Username**: admin



---```bash- **Password**: (tu password seguro)



## 📞 Info Proyectogit clone https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API.git



- **Repo:** [DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API](https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API)cd LAMBDA_proyectohotelsites_API#### 🚀 Ejecutar servidor:

- **Tipo:** Migración Power BI → Web App

- **Stack:** Django + React + TypeScript + PostgreSQL```

- **Estado:** Noviembre 2025 - En migración activa

```bash

---

### 2. Configuración del Backend (Django)python manage.py runserver

⚡ **Django + React + TypeScript** • 🔄 **Migración Power BI** • ⚠️ **Filtros y métricas requieren revisión**
```

```bash

# Navegar al directorio del backend**Backend disponible en**: `http://localhost:8000`

cd LAMBDA_proyecto_siteshotel/LAMBDA_backend_sites_hotels

### 3. Configuración del Frontend (React)

# Crear entorno virtual

python -m venv venv```bash

# Navegar al directorio del frontend

# Activar entorno virtual (Windows)cd LAMBDA_proyecto_siteshotel/LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotels

venv\Scripts\activate

# En macOS/Linux: source venv/bin/activate# Instalar dependencias

npm install

# Instalar dependencias

pip install -r requirements.txt# Configurar variables de entorno

cp .env.example .env

# Configurar variables de entorno```

cp .env.example .env

```#### 📝 Editar .env del frontend:



#### 📝 Editar `.env` con tus configuraciones:```env

VITE_API_URL=http://localhost:8000/api

```envVITE_ENV=development

SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-django```

DEBUG=True

FRONTEND_URL=http://localhost:3000#### 🚀 Ejecutar servidor de desarrollo:



# Base de datos PostgreSQL```bash

NAME_DATABASE=hoteldb_lambdanpm run dev

USER_DATABASE=postgres```

PASS_DATABASE=tu_password_postgresql

HOST_DATABASE=localhost**Frontend disponible en**: `http://localhost:3000`

PORT_DATABASE=5432

## 👥 Gestión de Usuarios - Guía Paso a Paso

# Configuración email (para notificaciones)

EMAIL_USE_TLS=True### 1. Acceder al Admin de Django

EMAIL_HOST=smtp.gmail.com

EMAIL_HOST_USER=tu_email@gmail.com1. Ve a: `http://localhost:8000/admin`

EMAIL_HOST_PASSWORD=tu_app_password_gmail2. Ingresa con el superusuario que creaste

EMAIL_PORT=5873. Verás el panel de administración de Django

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

```### 2. Crear Usuarios desde el Admin



#### 🗃️ Configurar base de datos PostgreSQL:1. **Ir a la sección "Usuarios"**:

   - Click en "Usuarios" en el panel izquierdo

```sql   - Click en "Agregar Usuario"

-- Conectar a PostgreSQL como superusuario

CREATE DATABASE hoteldb_lambda;2. **Completar información básica**:

CREATE USER tu_usuario WITH PASSWORD 'tu_password';   ```

GRANT ALL PRIVILEGES ON DATABASE hoteldb_lambda TO tu_usuario;   Email: usuario@lambda.com

```   Username: usuario_lambda

   Password: (password seguro)

#### 🔄 Ejecutar migraciones:   Password confirmation: (repetir password)

   ```

```bash

# Crear y aplicar migraciones3. **Configurar estado del usuario**:

python manage.py makemigrations   - ✅ Estado del usuario: Marcado (activo)

python manage.py migrate   - ✅ Staff status: Marcado (para acceso admin)

```   - ✅ Active: Marcado



**✅ La migración `0002_asignar_permisos_grupos.py` creará automáticamente:**### 3. Asignar Grupos y Permisos

- **Grupo "Admin"** - Permisos completos (crear, leer, actualizar, eliminar)

- **Grupo "Inversionista"** - Solo permisos de lectura (view)**Grupos disponibles automáticamente**:



#### 👤 Crear superusuario:#### 📋 **Grupo "Admin"**

- **Permisos**: Acceso completo (crear, leer, actualizar, eliminar)

```bash- **Uso**: Administradores del sistema

python manage.py createsuperuser- **Acceso**: Todas las funcionalidades

```

#### 📊 **Grupo "Inversionista"** 

Proporciona:- **Permisos**: Solo lectura (view)

- **Email**: admin@lambda.com (será el username)- **Uso**: Usuarios que solo consultan dashboards

- **Username**: admin- **Acceso**: Ver gráficas y reportes únicamente

- **Password**: (password seguro)

**Para asignar grupo al usuario**:

#### 🚀 Ejecutar servidor:1. En la página de edición del usuario

2. Buscar sección "Groups"

```bash3. Seleccionar el grupo apropiado (Admin o Inversionista)

python manage.py runserver4. Mover al campo "Chosen groups"

```5. Guardar usuario



**Backend disponible en**: `http://localhost:8000`### 4. Verificar Login en el Frontend

**Admin Django**: `http://localhost:8000/admin`

1. Ve a `http://localhost:3000`

### 3. Configuración del Frontend (React)2. Usa las credenciales del usuario creado

3. Verifica que accede según sus permisos

```bash

# Navegar al directorio del frontend (nueva terminal)## 📊 Dashboard y Métricas

cd LAMBDA_proyecto_siteshotel/LAMBDA_front_sites_hotels/LAMBDA_front_sites_hotels

### Datos Disponibles (Migrados de Power BI)

# Instalar dependencias

npm installEl sistema procesa archivos CSV con datos hoteleros:



# Configurar variables de entorno- **Ventas.csv**: Ingresos por alojamiento, fecha y propiedad

cp .env.example .env- **Habitaciones.csv**: Ocupación y disponibilidad

```- **Huespedes.csv**: Información de huéspedes

- **Forecast.csv**: Proyecciones RevPAR, ADR, ocupación

#### 📝 Editar `.env` del frontend:- **Expensas.csv**: Gastos operativos

- **Presupuesto.csv**: Presupuestos por periodo

```env- **Indicadoresppto.csv**: KPIs objetivo

VITE_API_URL=http://localhost:8000/api- **Propiedades.csv**: Catálogo de hoteles

VITE_ENV=development

```### Métricas Calculadas



#### 🚀 Ejecutar servidor de desarrollo:- **% Ocupación**: Habitaciones ocupadas / Total habitaciones

- **ADR (Average Daily Rate)**: Ingresos alojamiento / Habitaciones ocupadas

```bash- **RevPAR (Revenue per Available Room)**: Ingresos / Total habitaciones

npm run dev- **Cumplimiento Ocupación**: Ocupación real vs presupuestada

```- **Tarifa Promedio por Persona**: Ingresos / Número huéspedes



**Frontend disponible en**: `http://localhost:3000`### ⚠️ Problemas Conocidos en Migración



## 👥 Gestión de Usuarios - Guía Detallada1. **Filtros no sincronizados**: 

   - Los filtros de propiedad/concepto/periodo pueden no aplicarse correctamente

### 1. Acceder al Admin de Django   - **Revisión necesaria**: Validar query parameters en backend



1. **Ir a**: `http://localhost:8000/admin`2. **Cálculos de métricas**:

2. **Login** con el superusuario creado   - Algunas fórmulas de Power BI requieren ajustes

3. Verás el panel de administración Django   - **Revisar**: `dashboard/services/metrics_service.py`



### 2. Crear Usuarios desde el Admin3. **Formato de datos**:

   - CSV usan separador `|` (pipe) en lugar de coma

#### **Pasos detallados**:   - **Encoding**: latin1 para caracteres especiales



1. **En el panel admin** → Click en **"Usuarios"** (sección USUARIOS)## � Endpoints API Principales

2. **Click** en **"Agregar Usuario"** (botón verde)

3. **Completar formulario**:### Autenticación

   ``````

   Email: usuario@lambda.comPOST /api/auth/login/          # Login con email/password

   Username: usuario_lambdaPOST /api/auth/refresh/        # Renovar token JWT

   Password: password_seguro_123POST /api/auth/register/       # Registro de usuarios

   Password confirmation: password_seguro_123```

   ```

4. **Click "Guardar y continuar editando"**### Dashboard

```

### 3. Configurar Usuario CreadoGET /api/dashboard/metrics/    # Métricas principales

    ?property=all              # Filtro por propiedad

#### **En la página de edición del usuario**:    &concept=all              # Filtro por concepto  

    &period=month             # Periodo (month/quarter/year)

1. **Sección "Permissions"**:```

   - ✅ **Active**: Marcado (usuario activo)

   - ✅ **Staff status**: Marcado (acceso al admin)## � Tareas de Revisión Pendientes

   - ⚠️ **Superuser status**: Solo para administradores

### Backend (Prioridad Alta)

2. **Sección "Important dates"**: - [ ] **Validar filtros en metrics_service.py**

   - Se completa automáticamente  - Revisar si los parámetros `property`, `concept`, `period` se aplican correctamente

  - Validar queries de pandas en función de filtros

3. **Estado del usuario**:

   - ✅ **Estado del usuario**: Marcado (activo en el sistema)- [ ] **Verificar cálculos de KPIs**

  - Comparar resultados con Power BI original

### 4. Asignar Grupos y Permisos  - Validar fórmulas de ADR, RevPAR, ocupación



#### **Grupos disponibles (creados automáticamente)**:- [ ] **Optimizar carga de datos**

  - Los CSV se cargan en cada request (ineficiente)

##### 📋 **Grupo "Admin"**  - Implementar cache o base de datos

- **Permisos**: TODOS los permisos del sistema

- **Uso**: Administradores y personal técnico### Frontend (Prioridad Media)

- **Acceso**: Todas las funcionalidades + Django Admin- [ ] **Sincronización de filtros**

  - Verificar que FilterContext envíe parámetros correctos

##### 📊 **Grupo "Inversionista"**   - Validar que gráficas se actualicen con filtros

- **Permisos**: Solo permisos de lectura (`view_*`)

- **Uso**: Inversionistas y stakeholders- [ ] **Manejo de errores**

- **Acceso**: Solo consultar dashboards y reportes  - Mejorar feedback cuando métricas fallan

  - Loading states para carga de datos

#### **Para asignar grupo**:

1. **En la página del usuario** → Buscar sección **"Groups"**## 🚢 Comandos de Desarrollo

2. **En "Available groups"** → Seleccionar grupo apropiado

3. **Click en la flecha "→"** para mover a "Chosen groups"### Backend

4. **Guardar usuario**```bash

# Ejecutar servidor

### 5. Verificar Login en Frontendpython manage.py runserver



1. **Ir a**: `http://localhost:3000`# Ver logs de métricas (debug)

2. **Login** con las credenciales del usuario creadopython manage.py shell

3. **Verificar acceso** según permisos asignados>>> from dashboard.services.metrics_service import calculate_metrics

>>> calculate_metrics("all", "all", "month")

## 📊 Sistema de Dashboard - Detalles Técnicos

# Crear/aplicar migraciones

### Flujo de Datos (Como DEBERÍA Funcionar)python manage.py makemigrations

python manage.py migrate

```

Frontend FilterBar → FilterContext → useDashboardData → api.ts → Backend View → metrics_service.py → CSV Data# Crear superusuario adicional

```python manage.py createsuperuser

```

### Archivos CSV - Estructura de Datos Power BI

### Frontend

#### **Ubicación**: `dashboard/data/````bash

# Desarrollo con hot reload

1. **🏨 Habitaciones.csv** (18,026 registros)npm run dev

   - **Columnas**: `Titulo|Valor|Id|Fecha|Propiedad|Subconcepto|Concepto|General`

   - **Separador**: `|` (pipe)# Build para producción

   - **Encoding**: `latin1`npm run build

   - **Contenido**: Ocupación por habitación, fecha y propiedad

   - **Ejemplo**: `"Sites BAQ"|"Habitaciones ocupadas"|3|"2023-01-08"`# Preview del build

npm run preview

2. **💰 Ventas.csv** (9,945 registros)

   - **Columnas**: `"Titulo"|"Valor"|"Id"|"Fecha"|"Propiedad"`# Análisis de bundle

   - **Contenido**: Ingresos por concepto (ALOJAMIENTO, etc.)npm run build -- --analyze

   - **Ejemplo**: `"ALOJAMIENTO"|5830549|54|"2023-01-08"|"Sites BAQ"````



3. **📈 Forecast.csv**## � Seguridad y Autenticación

   - **Columnas**: RevPAR, ADR, Ocupación proyectada

   - **Uso**: Comparar rendimiento real vs proyecciones- **JWT Tokens**: Autenticación stateless

- **Renovación automática**: Tokens se renuevan antes de expirar

4. **👥 Huespedes.csv**- **Grupos y permisos**: Sistema granular de Django

   - **Contenido**: Número de huéspedes por fecha/propiedad- **CORS configurado**: Para comunicación frontend-backend

   - **Uso**: Cálculo de tarifa promedio por persona

## 📞 Contacto y Soporte

5. **🏢 Propiedades.csv**

   - **Contenido**: Catálogo de propiedades + Factor FARA- **Repositorio**: [LAMBDA_proyectohotelsites_API](https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API)

   - **Propiedades**: Sites 45, Sites BAQ, Sites MDE, Sites CTG, Sites SMR- **Organización**: DAVIDKNO-LAMBDA

- **Tipo**: Migración Power BI → Web App

### Métricas Calculadas

---

#### **Archivo**: `dashboard/services/metrics_service.py`

⚡ **Proyecto en migración activa - Django + React + TypeScript por LAMBDA**

**Métricas principales**:

- **% Ocupación**: `habitaciones_ocupadas / habitaciones_totales`🔄 **Última actualización**: Noviembre 2025 - En proceso de migración de Power BI

- **ADR**: `ingresos_alojamiento / habitaciones_ocupadas`
- **RevPAR**: `ingresos_alojamiento / habitaciones_totales`
- **Cumplimiento Ocupación**: `ocupacion_real / ocupacion_presupuestada`
- **Tarifa Promedio**: `ingresos_alojamiento / numero_huespedes`

## 🔥 PROBLEMAS CRÍTICOS - REQUIEREN ATENCIÓN INMEDIATA

### ❌ **Problema 1: Filtros No Se Aplican**

#### **Ubicación del problema**:
- **Frontend**: `src/contexts/FilterContext.tsx` líneas 40-50
- **Backend**: `dashboard/services/metrics_service.py` línea 48

#### **Qué está pasando**:
```python
# En metrics_service.py línea 48
def calculate_metrics(property_: str, concept: str, period: str):
    # ❌ PROBLEMA: Los parámetros NO se usan en el código
    # La función siempre procesa TODOS los datos sin filtrar
```

#### **Frontend envía**:
```typescript
// En useDashboardData.ts línea 15
const response = await apiService.getDashboardMetrics(property, area, period);
// Envía: property="sites45", area="alojamiento", period="month"
```

#### **Backend NO aplica filtros**:
```python
# Debería filtrar por propiedad, pero NO lo hace
ventas = d["ventas"]  # ❌ Toma TODOS los datos
# Debería ser:
# ventas = d["ventas"].query("Propiedad == @property_") si property_ != "all"
```

#### **Solución requerida**:
```python
# En metrics_service.py, agregar filtros:
if property_ != "all":
    ventas = ventas.query("Propiedad == @property_")
    habitaciones = habitaciones.query("Propiedad == @property_")
    # etc. para todos los DataFrames
```

### ❌ **Problema 2: Gráficas Usan Datos Falsos**

#### **Ubicación del problema**:
- **Archivo**: `src/lib/dummyData.ts`
- **Componentes afectados**: Todos en `src/components/dashboard/`

#### **Qué está pasando**:
```tsx
// En Dashboard.tsx líneas 24-30
import {
  salesTrendData,        // ❌ Datos falsos
  occupancyTrendData,    // ❌ Datos falsos  
  avgRateTrendData,      // ❌ Datos falsos
  // ...
} from "@/lib/dummyData";
```

#### **Solución requerida**:
1. **Eliminar** importación de `dummyData.ts`
2. **Crear endpoints** para datos de gráficas en backend
3. **Conectar gráficas** a datos reales del API

### ❌ **Problema 3: Cálculos de Power BI No Coinciden**

#### **Ubicación del problema**:
- **Archivo**: `dashboard/services/metrics_service.py` líneas 60-150

#### **Métricas que necesitan revisión**:

1. **% Ocupación** (líneas 60-64):
   ```python
   # ❌ REVISAR: Query podría estar mal
   hab_ocupadas = habitaciones.query('Subconcepto == "Habitaciones ocupadas"')["Valor"].sum()
   hab_totales = habitaciones.query('General == "Habitaciones totales"')["Valor"].sum()
   ```

2. **ADR - Average Daily Rate** (líneas 74-77):
   ```python
   # ❌ REVISAR: Fórmula vs Power BI
   adr = safe_div(ventas_alo, hab_ocupadas)
   ```

3. **RevPAR** (líneas 78-80):
   ```python
   # ❌ REVISAR: Comparar con Power BI
   revpar = safe_div(ventas_alo, hab_totales)
   ```

#### **Pasos para validar**:
1. **Comparar resultados** con Power BI original
2. **Revisar fórmulas** específicas de cada métrica
3. **Validar queries** de pandas con estructura CSV
4. **Ajustar cálculos** según sea necesario

## 🔧 Endpoints API Disponibles

### **Autenticación**
```
POST /api/usuarios/login/          # Login con email/password
POST /api/usuarios/refresh/        # Renovar token JWT  
POST /api/usuarios/register/       # Registro usuarios
```

### **Dashboard**
```
GET /api/dashboard/metrics/        # ⚠️ Métricas (filtros no funcionan)
    ?property=sites45              # Parámetro ignorado
    &concept=alojamiento          # Parámetro ignorado
    &period=month                 # Parámetro ignorado
```

## 🛠️ Tareas de Desarrollo Pendientes

### 🔥 **Prioridad CRÍTICA**

- [ ] **Implementar filtros en backend**
  - Archivo: `dashboard/services/metrics_service.py`
  - Aplicar parámetros `property_`, `concept`, `period` en queries
  - Validar que filtros funcionen correctamente

- [ ] **Conectar gráficas a datos reales**
  - Eliminar dependencia de `dummyData.ts`
  - Crear endpoints específicos para datos de gráficas
  - Actualizar componentes dashboard

- [ ] **Validar cálculos vs Power BI**
  - Comparar cada métrica con Power BI original
  - Ajustar fórmulas según sea necesario
  - Documentar diferencias encontradas

### 📋 **Prioridad ALTA**

- [ ] **Optimizar carga de datos**
  - Los CSV se cargan en cada request (ineficiente)
  - Implementar cache o migrar a base de datos
  - Mejorar performance general

- [ ] **Manejo de errores**
  - Mejorar feedback cuando métricas fallan
  - Agregar loading states en frontend
  - Validación de datos CSV

### 📊 **Prioridad MEDIA**

- [ ] **Ampliar dashboard funcionalidades**
  - Exportar reportes
  - Dashboards por rol de usuario
  - Notificaciones automáticas

## 🚢 Comandos de Desarrollo

### **Backend**
```bash
# Ejecutar servidor
python manage.py runserver

# Debug métricas (para probar cálculos)
python manage.py shell
>>> from dashboard.services.metrics_service import calculate_metrics
>>> result = calculate_metrics("sites45", "alojamiento", "month")
>>> print(result)

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear usuarios adicionales
python manage.py createsuperuser
```

### **Frontend**
```bash
# Desarrollo con hot reload
npm run dev

# Build para producción
npm run build

# Análisis del bundle
npm run build -- --analyze

# Linting
npm run lint
```

## 🔐 Autenticación y Seguridad

- **JWT Tokens**: Autenticación stateless
- **Renovación automática**: En `api.ts` líneas 100-140
- **Grupos automáticos**: Creados en migración `0002_asignar_permisos_grupos.py`
- **CORS configurado**: Para desarrollo local

## 📞 Contacto y Repositorio

- **GitHub**: [DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API](https://github.com/DAVIDKNO-LAMBDA/LAMBDA_proyectohotelsites_API)
- **Organización**: DAVIDKNO-LAMBDA
- **Tipo de proyecto**: Migración Power BI → Aplicación Web

---

## 📋 Checklist de Revisión

### ✅ **Completado**
- [x] Autenticación JWT
- [x] Grupos y permisos de usuario
- [x] Estructura básica frontend/backend
- [x] Carga básica de datos CSV

### ⚠️ **En Desarrollo - REQUIERE ATENCIÓN**
- [ ] 🔥 **Filtros funcionales** (Crítico)
- [ ] 🔥 **Métricas precisas** (Crítico)  
- [ ] 🔥 **Gráficas con datos reales** (Crítico)
- [ ] Performance y optimización
- [ ] Validación completa vs Power BI

---

⚡ **Proyecto en migración activa - Django + React + TypeScript por LAMBDA**

🔄 **Estado**: Noviembre 2025 - Migración Power BI en proceso

⚠️ **Nota importante**: Este README identifica específicamente las áreas que requieren atención para completar la migración exitosa de Power BI a la aplicación web.