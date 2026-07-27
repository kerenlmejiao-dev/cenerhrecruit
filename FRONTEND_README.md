# 🚀 CENERH RECRUIT OS - Frontend

Portal web profesional para evaluación de candidatos + Dashboard admin.

---

## 📦 Requisitos

- Node.js 18+ 
- npm o yarn
- Backend API corriendo (http://localhost:8000)

---

## 🚀 Inicio rápido

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env.local
# Editar .env.local con tu API URL
```

### 3. Iniciar desarrollo

```bash
npm run dev
```

El frontend estará en: http://localhost:5173

---

## 📁 Estructura del proyecto

```
frontend/
├── src/
│   ├── pages/
│   │   ├── RegistroPage.jsx      # Página de registro
│   │   ├── TestsPage.jsx         # Responder tests
│   │   ├── ResultadosPage.jsx    # Ver scores
│   │   └── AdminDashboard.jsx    # Panel admin
│   ├── services/
│   │   └── api.js                # Cliente API
│   ├── App.jsx                   # Componente principal
│   ├── main.jsx                  # Punto de entrada
│   └── index.css                 # Estilos Tailwind
├── index.html                    # Plantilla HTML
├── package.json                  # Dependencias
├── vite.config.js               # Config Vite
├── tailwind.config.js           # Config Tailwind
└── postcss.config.js            # Config PostCSS
```

---

## 🎯 Páginas

### 1. Registro (`/`)
- Candidatos se registran
- Ingresan nombre, email, teléfono
- Seleccionan vacante
- Pasa a tests

### 2. Tests (`/tests`)
- Preguntas psicométricas
- Barra de progreso
- Guardado automático
- Navegación entre tests

### 3. Resultados (`/resultados`)
- Score final
- Scores por test
- Gráficos de desempeño
- Descargar PDF
- Enviar por email

### 4. Admin (`/admin`)
- Dashboard CENERH
- KPIs de candidatos
- Tabla filtrable
- Ver PDFs

---

## 🛠️ Desarrollo

### Agregar una nueva página

```jsx
// src/pages/NuevaPage.jsx
export default function NuevaPage() {
  return (
    <div>
      Contenido
    </div>
  );
}

// Agregar ruta en App.jsx
<Route path="/nueva" element={<NuevaPage />} />
```

### Llamar a la API

```jsx
import { candidatosAPI, testsAPI } from '../services/api';

// Crear candidato
const resultado = await candidatosAPI.crear({
  nombre: 'Juan',
  email: 'juan@example.com',
  vacante_id: 'contador_paraiso'
});

// Obtener tests
const tests = await testsAPI.obtenerDisponibles();
```

### Estilos Tailwind

```jsx
// Usar clases Tailwind
<div className="bg-blue-600 text-white p-4 rounded-lg">
  Contenido
</div>

// Colores CENERH
<div className="bg-cenerh-blue text-white">
  Azul institucional
</div>
```

---

## 📦 Build para producción

```bash
npm run build
```

Genera carpeta `dist/` lista para deploy.

---

## 🚀 Deploy

### Opción 1: Vercel (Recomendado)

```bash
npm i -g vercel
vercel
```

### Opción 2: Netlify

```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

### Opción 3: Servidor propio

```bash
# Instalar servidor HTTP
npm install -g http-server

# Servir dist/
http-server dist/
```

---

## 🔗 Integración API

El frontend se conecta a la API backend via `src/services/api.js`.

### Variables de entorno

```
VITE_API_URL=http://localhost:8000  # Desarrollo
VITE_API_URL=https://api.tudominio.com  # Producción
```

### Endpoints utilizados

```
POST   /api/candidatos                    # Crear candidato
GET    /api/tests/disponibles             # Obtener tests
GET    /api/tests/{id}/info              # Info del test
GET    /api/tests/{id}/{candidato_id}    # Obtener preguntas
POST   /api/tests/{id}/{candidato_id}/respuestas  # Guardar respuestas
GET    /api/candidatos/{id}/resultados   # Obtener resultados
GET    /api/candidatos/{id}/ficha.pdf    # Descargar PDF
POST   /api/candidatos/{id}/email        # Enviar email
```

---

## 🎨 Personalización

### Colores corporativos

En `tailwind.config.js`:

```js
colors: {
  'cenerh-blue': '#0050A0',
  'cenerh-red': '#D62828',
  'cenerh-gold': '#C9A14A',
}
```

### Tipografía

En `index.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700');
```

---

## 🧪 Testing

```bash
# Placeholder para tests futuros
npm run test
```

---

## 📱 Responsive

El frontend es 100% responsive:
- Mobile: 320px+
- Tablet: 768px+
- Desktop: 1024px+

---

## 🔒 Seguridad

- ✅ Variables de entorno en .env.local (no commitear)
- ✅ CORS configurado en backend
- ✅ Validación en frontend y backend
- ✅ Sin guardar datos sensibles en localStorage (solo ID)

---

## 📊 Performance

- ✅ Code splitting automático con Vite
- ✅ Lazy loading de componentes (opcional)
- ✅ Minificación en build
- ✅ CSS purificado con Tailwind

---

## 🐛 Debugging

### Ver logs

```jsx
// En terminal
console.log('Debug:', variable);

// En navegador: F12 → Console
```

### Network

F12 → Network → Ver requests a API

---

## 📚 Recursos

- React: https://react.dev
- Vite: https://vitejs.dev
- Tailwind: https://tailwindcss.com
- React Router: https://reactrouter.com
- Axios: https://axios-http.com

---

## ✅ Checklist de Deploy

- [ ] Backend corriendo en producción
- [ ] Variables de entorno configuradas
- [ ] npm run build sin errores
- [ ] dist/ generado correctamente
- [ ] CORS habilitado en backend
- [ ] API responde en producción
- [ ] HTTPS configurado
- [ ] DNS apunta al frontend

---

## 💬 Soporte

Para ayuda:
1. Ver logs en consola (F12)
2. Revisar network (F12 → Network)
3. Verificar .env.local
4. Verificar que API está corriendo

---

## 🎉 ¡Listo!

Tu frontend está listo para candidatos. Próximo paso: Deploy en producción.
