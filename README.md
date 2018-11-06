# Word2Vec Bahasa Indonesia

Word2Vec untuk bahasa Indonesia dari dataset Wikipedia

## Installation
```bash
git clone https://github.com/deryrahman/word2vec-bahasa-indonesia.git
cd word2vec-bahasa-indonesia
pip install -r requirements.txt
```

## Train
```bash
python train.py
```
Some useful arguments
```bash
usage: train.py [-h] [--model_path MODEL_PATH]
                [--extracted_path EXTRACTED_PATH] [--dump_path DUMP_PATH]
                [--dim DIM] [--stem STEM]

Word2Vec: Generating word2vec model for bahasa Indonesia

optional arguments:
  -h, --help                        show this help message and exit
  --model_path MODEL_PATH           path for saving trained models
  --extracted_path EXTRACTED_PATH   path for extracting text
  --dump_path DUMP_PATH             path for dump data
  --dim DIM                         embedding size
  --stem STEM                       use stemmer or not. (default false)
```

## Model
You can use a trained model on the folder model

---

## License

Open sourced under the [MIT license](LICENSE.md).
