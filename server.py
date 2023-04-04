import pickle
from fastapi import FastAPI
from models.post import Post
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.utils import CustomTokenizer, check_obscene

app = FastAPI(title='TG Post Classifier API',
              description='API for TG post classification using ML',
              version='0.1')

# инициализируем логгирование
clf_API_logger = logging.getLogger()
clf_API_logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, filename='clf_API_logs.log')

model = None
toxic_vocab = None
obscene_vocab = None
vec = None


@app.on_event('startup')
def load_all():
    global model
    global toxic_vocab
    global vec
    global obscene_vocab
    model = pickle.load(open('models/toxic_model.pkl', 'rb'))
    toxic_vocab = pickle.load(open('models/toxic_vocab.pkl', 'rb'))
    obscene_vocab = pickle.load(open('models/obscene_vocab.pkl', 'rb'))
    vec = TfidfVectorizer(tokenizer=CustomTokenizer(), vocabulary=toxic_vocab)


@app.post('/api', tags=['prediction'])
async def get_prediction(post: Post):
    try:
        post_types = {
            0: 'non_toxic',
            1: 'toxic'
        }

        if check_obscene(post.message, obscene_vocab):
            return {'toxic': 'toxic', 'obscene': 'obscene'}

        data_vec = vec.fit_transform([post.message])

        toxic_predictions = list(map(lambda x: post_types.get(x), model.predict(data_vec).tolist()))

        return {'toxic': toxic_predictions[0], 'obscene': 'non_obscene'}

    except ValueError:
        clf_API_logger.error('Something wrong with predictions')
        return {'toxic': 'error', 'obscene': 'error'}
