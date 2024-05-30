__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IRag(ABC):

    @property
    @abstractmethod
    def trace(self):
        pass
    
    @abstractmethod
    def readTXT(self, txtfile):
        pass
    
    @abstractmethod
    def readPDF(self, pdffile, method):
        pass
    
    @abstractmethod
    def charChunk(self, doc, separator, chunk_size, chunk_overlap):
        pass
    
    @abstractmethod
    def semChunk(self, doc):
        pass
    
    @abstractmethod
    def buildPrompt(self, question, nr):
        pass
    
    @abstractmethod
    def promptLLM(self, question, urlOllama, model, temperature):
        pass
    
    @abstractmethod
    def createEmbeddings(self, cks):
        pass
    
    @abstractmethod
    def initSearchEngine(self):
        pass
    
    @abstractmethod
    def processSearch(self, k, vPrompt):
        pass
    
    @abstractmethod
    def addEmbeddings(self, vChunks):
        pass