from tempfile import NamedTemporaryFile
from sklearn.ensemble import RandomForestRegressor  # noqa: F401
from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from analyzer import ChartAnalyzer
from dataclasses import dataclass
import pickle


@dataclass
class DifficultyResponse():
    difficulty: float


analyzer = ChartAnalyzer()
predictor = pickle.load(open('difficulty_model.sav', 'rb'))
app = FastAPI(
    title='Sonolus difficulty server',
    description='SUSファイルから難易度を推定するサーバー',
    version='0.1.0'
)


@app.get('/health_check')
async def health_check():
    """生存確認用エンドポイント"""
    return {'message': 'Server is working'}


@app.post('/predict', response_model=DifficultyResponse)
async def predict_difficulty(file: UploadFile):
    """SUSファイルから難易度を推定するエンドポイント"""
    if not file.filename.endswith('.sus') or\
            not file.content_type == 'application/octet-stream':
        return {'message': 'Invalid file format'}
    with NamedTemporaryFile('wb', delete=False) as f:
        content = await file.read()
        f.write(content)
        f.seek(0)
        data = analyzer.get_feature_values_from_sus(f.name)
        result = predictor.predict([data])
    return DifficultyResponse(difficulty=result[0])

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
