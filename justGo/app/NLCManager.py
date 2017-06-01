from .config.config import Config
from watson_developer_cloud import NaturalLanguageClassifierV1
import requests
import json

class Singleton(type):
  instance = None

  def __call__(cls, *args, **kwargs):
    if not cls.instance:
      cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
    return cls.instance

class NLCManager(metaclass=Singleton):
  natural_language_classifier = NaturalLanguageClassifierV1(
  username = Config.NLC_USERNAME,
  password = Config.NLC_PASSWORD) 

  def analysis(self, message):
    classes = self.natural_language_classifier.classify(Config.NLC_Classifier_ID,message) 
    return classes['top_class']

