"""
FastAPI приложение для обработки файлов через Perplexity API.
"""

import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from wpd.init_core import init_core

app = FastAPI(title="ГУАП - Формирование учебной программы")

# Папка для временных файлов и результатов
UPLOAD_DIR = Path("files/uploads")
RESULT_DIR = Path("files/results")
TEMPLATE_PATH = Path("files/Шаблон.docx")

# Создаем папки если их нет
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Главная страница с формой загрузки."""
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ГУАП - Формирование учебной программы</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
                font-size: 28px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 16px;
            }
            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                margin-bottom: 20px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .upload-area:hover {
                background-color: #f8f9ff;
                border-color: #764ba2;
            }
            .upload-area.dragover {
                background-color: #e8ebff;
                border-color: #764ba2;
            }
            input[type="file"] {
                display: none;
            }
            .file-label {
                display: inline-block;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: transform 0.2s ease;
            }
            .file-label:hover {
                transform: scale(1.05);
            }
            .file-name {
                margin-top: 15px;
                color: #333;
                font-weight: 500;
            }
            .file-name.empty {
                color: #999;
                font-style: italic;
            }
            button {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                margin-top: 20px;
            }
            button:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .download-btn {
                display: none;
                margin-top: 20px;
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            }
            .download-btn.show {
                display: block;
            }
            .status {
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                font-weight: 500;
                display: none;
            }
            .status.show {
                display: block;
            }
            .status.processing {
                background-color: #fff3cd;
                color: #856404;
            }
            .status.success {
                background-color: #d4edda;
                color: #155724;
            }
            .status.error {
                background-color: #f8d7da;
                color: #721c24;
            }
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ГУАП</h1>
            <p class="subtitle">Формирование учебной программы</p>
            
            <div class="upload-area" id="uploadArea">
                <input type="file" id="fileInput" accept=".docx" />
                <label for="fileInput" class="file-label">Загрузить учебник</label>
                <div class="file-name empty" id="fileName">Файл не выбран</div>
            </div>
            
            <button id="submitBtn" onclick="submitFile()" disabled>Отправить</button>
            
            <div class="status" id="status"></div>
            
            <a id="downloadBtn" class="download-btn" href="#" download style="display: none; text-decoration: none; color: white; text-align: center; padding: 15px; border-radius: 25px; font-size: 18px; font-weight: 600; margin-top: 20px;">
                Скачать результат
            </a>
        </div>
        
        <script>
            const fileInput = document.getElementById('fileInput');
            const fileName = document.getElementById('fileName');
            const submitBtn = document.getElementById('submitBtn');
            const uploadArea = document.getElementById('uploadArea');
            const status = document.getElementById('status');
            const downloadBtn = document.getElementById('downloadBtn');
            
            // Обработка выбора файла
            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    fileName.textContent = file.name;
                    fileName.classList.remove('empty');
                    submitBtn.disabled = false;
                } else {
                    fileName.textContent = 'Файл не выбран';
                    fileName.classList.add('empty');
                    submitBtn.disabled = true;
                }
            });
            
            // Drag and drop
            uploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    fileInput.files = files;
                    fileInput.dispatchEvent(new Event('change'));
                }
            });
            
            // Отправка файла
            async function submitFile() {
                const file = fileInput.files[0];
                if (!file) {
                    alert('Пожалуйста, выберите файл');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                submitBtn.disabled = true;
                status.className = 'status processing show';
                status.innerHTML = '<div class="spinner"></div><br>Обработка файла...';
                downloadBtn.style.display = 'none';
                
                try {
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Ошибка при обработке файла');
                    }
                    
                    const result = await response.json();
                    
                    status.className = 'status success show';
                    status.textContent = 'Файл успешно обработан!';
                    
                    downloadBtn.href = `/download/${result.file_id}`;
                    downloadBtn.style.display = 'block';
                    
                } catch (error) {
                    status.className = 'status error show';
                    status.textContent = 'Ошибка: ' + error.message;
                } finally {
                    submitBtn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Загружает файл от пользователя и обрабатывает его через ядро.
    
    Returns:
        dict с file_id для скачивания результата
    """
    # Проверяем расширение файла
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Поддерживаются только файлы .docx")
    
    # Генерируем уникальный ID для сессии
    file_id = str(uuid.uuid4())
    
    # Сохраняем загруженный файл
    uploaded_file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(uploaded_file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Путь к шаблону (фиксированный)
        template_path = str(TEMPLATE_PATH)
        if not Path(template_path).exists():
            raise HTTPException(
                status_code=500,
                detail=f"Шаблон не найден: {template_path}"
            )
        
        # Путь к результату
        result_path = RESULT_DIR / f"{file_id}_result.docx"
        
        # Промпт для заполнения переменных
        prompt = (
            "Привет, ты профессиональный эксперт-методист с 15-летним стажем работы в сфере. "
            "Я прикрепляю для тебя 2 файла: шаблон Рабочей программы дисциплины от ВУЗа, а также учебные материалы. "
            "Тебе нужно заполнить шаблон Рабочей программы дисциплины, основываясь на учебных материалах, "
            "которые содержат всё, что планируется реализовать в программе на семестр. "
            "Для того, чтобы это сделать, для начала тебе нужно проанализировать шаблон и то, чего там не хватает "
            "(что нужно заполнить) (все эти места являются как бы переменными и отмечены двойными фигурными скобками, "
            "внутри них содержится краткое описание того, что там должно быть), а затем, проанализировав учебные материалы, "
            "найти те недостающие 'переменные', которые нужно заполнить в шаблоне. "
            "Ты должен выбрать и вернуть мне именно то, что непосредственно прямо указано в материалах. "
            "Те переменные, которые там не упоминаются, или которые ты не смог найти - просто пропускай и не вноси в финальный результат, "
            "который ты будешь возвращать мне. "
            "Возвращать данные мне ты должен в формате ключ:значение; ключ:значение;..., "
            "где ключ - это полное название переменной, как в шаблоне, а значение - то значение, которое ты для нее нашел. "
            "Не добавляй в ответ никакие специальные символы, разделения строк и так далее. "
            "Когда выводишь список переменных и их значений не оборачивай ключи или значения в спец символы. "
            "Символ новой строки после знака точки с запятой тоже ставить не нужно"
        )
        
        # Вызываем функцию из ядра
        # Теперь file1_path - это шаблон (фиксированный), file2_path - загруженный файл пользователя
        init_core(
            file1_path=str(template_path),  # Шаблон РПД
            file2_path=str(uploaded_file_path),  # Загруженный учебник от пользователя
            prompt=prompt,
            model="sonar",
            template_path=str(template_path),
            result_path=str(result_path),
        )
        
        return {"file_id": file_id, "message": "Файл успешно обработан"}
        
    except Exception as e:
        # Удаляем загруженный файл при ошибке
        if uploaded_file_path.exists():
            uploaded_file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Скачивает обработанный файл result.docx.
    
    Args:
        file_id: ID файла из ответа /upload
        
    Returns:
        FileResponse с файлом result.docx
    """
    result_file = RESULT_DIR / f"{file_id}_result.docx"
    
    if not result_file.exists():
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(
        path=str(result_file),
        filename="result.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@app.on_event("startup")
async def startup_event():
    """Событие запуска приложения"""
    print("Веб-сервер запущен на http://localhost:8000")


if __name__ == "__main__":
    import uvicorn
    print("Запуск веб-сервера...")
    print("Для запуска с Telegram ботом используйте: python run_all.py")
    uvicorn.run(app, host="0.0.0.0", port=8000)

