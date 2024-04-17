
import pandas as pd
from flask import Flask, request, jsonify
from models.malicious_url_detection import predict_url_type, load_malicious_url_model
from models.content_moderation import predictors, predict_fraudulent, load_content_moderation_models , spacy_tokenizer
app = Flask(__name__)




@app.route('/externalUrl', methods=['POST'])
def predict_externalUrl():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL not provided'}), 400
    model = load_malicious_url_model()
    predicted_type = predict_url_type(url,model)
    return jsonify({'predicted_type': predicted_type})

@app.route('/contentModeration', methods=['POST'])
def predict_content():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Data not provided'}), 400
    # #Construct DataFrame from JSON data
    # df = pd.DataFrame(data)
    # # Make prediction
    # predictions = predict_fraudulent(df, load_content_moderation_models())
    # result = {
    #     'predictions': predictions
    # }
    # return jsonify(result)

    try:
        # Construct DataFrame from JSON data
        df = pd.DataFrame(data)
        # Make prediction
        predictions = predict_fraudulent(df, load_content_moderation_models())
        result = {
            'predictions': predictions
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
