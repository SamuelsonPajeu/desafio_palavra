from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup
import logging
import toml
import pathlib
import time
import json
import warnings


@dataclass(frozen=False)
class Colector:
    searched_word: str
    words: dict = field(default_factory=dict, init=False, repr=False)
    urls: dict = field(default_factory=dict, init=False, repr=False)

    def start(self):
        logging.info(f"[Colector/SearchWord] Searching for '{self.searched_word}'...")

        # Primeiro procura se a palavra já foi buscada e está no arquivo de cache
        cache = CachedWords()
        logging.debug(f"[Colector/SearchWord] Cache: {cache.words}")

        if cache.__contains__(self.searched_word):
            logging.info(f"[Colector/SearchWord] '{self.searched_word}' found in cache...")
            logging.info(f"[Colector/SearchWord] Got {cache.get(self.searched_word)['total_ammount']} words from {self.searched_word}...")
            cache.words[self.searched_word]["searches"] += 1
            return {self.searched_word: cache.get(self.searched_word)}

        # Começo do Coletor - Pega o tempo que o programa foi iniciado
        logging.info(f"[Colector/SearchWord] Word {self.searched_word} is not in cache, collecting...")
        start = time.perf_counter()
        # Carrega o arquivo config.toml e pega as urls
        self.load_config()

        # Pra cada tipo de palavra relacionada, faz um request para a url e pega as palavras
        for i in self.urls:
            self.get_word(i, self.urls[i]["class"])
        self.words[self.searched_word]['total_ammount'] = sum([self.words[self.searched_word][i]['ammount'] for i in self.words[self.searched_word]])
        self.words[self.searched_word]['searches'] = 1

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            debug_words = json.dumps(self.words[self.searched_word], sort_keys=True, indent=4, ensure_ascii=False)

            with open("generated_data.json", "w") as f:
                json.dump(self.words[self.searched_word], f, sort_keys=True, indent=4, ensure_ascii=False)
            logging.debug(f"[Colector/SearchWord] Related words from {self.searched_word} got: {debug_words}")
        logging.info(f"[Colector/SearchWord] Got {self.words[self.searched_word]['total_ammount']} related words from '{self.searched_word}'...")

        # Tempo de execução final do coletor
        end = time.perf_counter()
        logging.info(f"[Colector/SearchWord] Search for '{self.searched_word}' finished in {end - start:0.4f} seconds")

        # Adiciona a palavra buscada ao cache
        cache.add(self.searched_word, self.words[self.searched_word])

        # Retorna as palavras relacionadas
        return self.words

    def load_config(self):
        logging.info("[Colector/load_config] Loading config file...")

        # Carrega o arquivo config.toml e adiciona as urls para serem utilizadas pela Classe
        _toml_data = toml.load(pathlib.Path(__file__).parent / "config.toml")
        for i in _toml_data["urls"]:
            self.urls[i] = _toml_data["urls"][i]
        self.words[self.searched_word] = {}

        logging.debug(f"[Colector/load_config] Config file loaded: {self.urls}")
        logging.info("[Colector/load_config] Loading done...")

    def get_word(self, _type, _class):
        logging.info(f"[Colector/get_word] Getting related {_type} from {self.searched_word}...")
        # Recebe o tipo de palavra relacionada que será buscada (Substantivo, Verbo, Adjetivo) e faz um request para a url
        request_content = requests.get(self.urls[_type]["link"].format(self.searched_word))
        soup = BeautifulSoup(request_content.content, 'html.parser')
        related_words = soup.find_all('ul', class_=_class)

        # Pega todas as palavras encontradas e adiciona ao dicionário de palavras
        self.words[self.searched_word][_type] = {
            "words": [],
            "ammount": 0,
        }

        max_results = toml.load(pathlib.Path(__file__).parent / "config.toml")["search"]["max_results"]
        for i in related_words:
            self.words[self.searched_word][_type]["words"] += [
                                                                j.text for j in i.find_all('a')
                                                                if j.text
                                                                and j.text != self.searched_word
                                                                and len(self.words[self.searched_word][_type]["words"]) < max_results
                                                            ]
        self.words[self.searched_word][_type]["ammount"] = len(self.words[self.searched_word][_type]["words"])

        logging.debug(f"[Colector/get_word] Related {_type} from {self.searched_word} got: {self.words[self.searched_word][_type]}")
        logging.info(f"[Colector/get_word] Got {len(self.words[self.searched_word][_type]['words'])} {_type}s from {self.searched_word}...")


class FormatNotSupported(Exception):
    logging.error("[CachedWords/FormatNotSupported] Format not supported")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CachedWords(metaclass=Singleton):

    def __init__(self):
        self.words = {}
        self.config = toml.load(pathlib.Path(__file__).parent / "config.toml")
        self.enabled = self.config["cache"]["enabled"]
        self.max_size = self.config["cache"]["max_size"]

    def add(self, word, data):
        if not isinstance(data, dict) or not isinstance(word, str):
            raise FormatNotSupported
        if not self.enabled:
            warnings.warn("[CachedWords/add] Cache is disabled, not adding to cache, enable it in config.toml")
            return
        if len(self.words) >= self.max_size:
            less_searched = self.get_less_searched()
            logging.warning(f"[CachedWords/add] Cache is full, removing less searched word {less_searched}...")
            self.remove(less_searched)
        logging.info(f"[CachedWords/add] Adding {word} to cache...")
        self.words[word] = data

    def get_less_searched(self):
        searches = {self.words[key]["searches"]: key for key in self.words}
        return searches[min(searches)]

    def remove(self, word):
        if not isinstance(word, str):
            raise FormatNotSupported

        logging.info(f"[CachedWords/remove] Removing {word} from cache...")
        try:
            del self.words[word]
        except KeyError:
            logging.warning(f"[CachedWords/remove] Word {word} not found in cache")

    def get(self, word):
        return self.words.get(word) if self.enabled else False

    def count_total(self):
        return len(self.words.keys()) if self.enabled else 0

    def __contains__(self, word):
        return word in self.words if self.enabled else False
