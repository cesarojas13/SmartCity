# Smart City AI Challenge — versión sin Service Account

Esta versión guarda el ranking en Google Sheets usando un Webhook de Google Apps Script.

No usa:
- Service Accounts
- Llaves JSON
- Google Cloud IAM

## Archivos para GitHub

```text
app.py
requirements.txt
README.md
```

## Archivo adicional

```text
apps_script.gs
```

Ese archivo se pega en Google Sheets > Extensiones > Apps Script.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configurar Google Sheets + Apps Script

1. Crea un Google Sheet llamado `Smart City AI Challenge Ranking`.
2. Entra a `Extensiones > Apps Script`.
3. Borra el contenido existente.
4. Pega el contenido de `apps_script.gs`.
5. Guarda el proyecto.
6. Presiona `Deploy > New deployment`.
7. Tipo: `Web app`.
8. Execute as: `Me`.
9. Who has access: `Anyone`.
10. Copia la URL que termina en `/exec`.

## Configurar Streamlit Secrets

En Streamlit Cloud:

```text
App > Settings > Secrets
```

Agrega:

```toml
apps_script_webhook_url = "https://script.google.com/macros/s/TU_URL/exec"
```

Luego reinicia la app.

## Prueba

1. Juega una partida completa.
2. Al final debe aparecer `Resultado guardado en el ranking`.
3. En Google Sheets debe aparecer una hoja llamada `Ranking` con el resultado.