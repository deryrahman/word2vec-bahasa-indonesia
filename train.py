import gensim
import multiprocessing
import os.path
import requests
import argparse
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys

def download(link, file_name):
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()

def get_id_wiki(dump_path):
    if not os.path.isfile(dump_path):
        url = 'https://dumps.wikimedia.org/idwiki/latest/idwiki-latest-pages-articles.xml.bz2'
        download(url, dump_path)
    return gensim.corpora.WikiCorpus(dump_path, lemmatize=False, dictionary={})

def extract_text(extracted_path, id_wiki, stem):
    if os.path.isfile(extracted_path):
        return None
    if stem:
        print('Warning : Using stemmer could slow down the extracting progress')
        stemmer = StemmerFactory().create_stemmer()
    with open(extracted_path, 'w') as f:
        i = 0
        for text in id_wiki.get_texts():
            text = ' '.join(text)
            text = stemmer.stem(text) if stem else text
            f.write(text + '\n')
            i += 1
            if i%(10 if stem else 1000) == 0:
                print(str(i), 'articles processed')
        print('total:', str(i))
    return None

def build_model(extracted_path, model_path, dim):
    sentences = gensim.models.word2vec.LineSentence(extracted_path)
    id_w2v = gensim.models.word2vec.Word2Vec(sentences, size=dim, workers=multiprocessing.cpu_count()-1)
    id_w2v.save(model_path)
    return id_w2v

def main(args):
    model_path = args.model_path
    extracted_path = args.extracted_path
    dump_path = args.dump_path
    dim = args.dim
    stem = args.stem
    id_wiki = get_id_wiki(dump_path)
    print('Extracting text...')
    extract_text(extracted_path, id_wiki, stem)
    print('Build a model...')
    build_model(extracted_path, model_path, dim)
    print('Saved model:', model_path)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Word2Vec: Generating word2vec model for bahasa Indonesia')
    parser.add_argument('--model_path', type=str, default='./model/idwiki_word2vec.model',
                        help='path for saving trained models')
    parser.add_argument('--extracted_path', type=str, default='./data/idwiki.txt',
                        help='path for extracting text')
    parser.add_argument('--dump_path', type=str, default='./data/idwiki-latest-pages-articles.xml.bz2',
                        help='path for dump data')
    parser.add_argument('--dim', type=int, default=100,
                        help='embedding size')
    parser.add_argument('--stem', default=False, type=lambda x: (str(x).lower() == 'true'),
                        help='use stemmer or not. (default false)')
    args = parser.parse_args()
    main(args)
