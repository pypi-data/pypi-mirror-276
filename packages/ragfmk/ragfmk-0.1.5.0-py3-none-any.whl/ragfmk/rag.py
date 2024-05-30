__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from ragfmk.elements.wrappers.document import document
from ragfmk.elements.llms.ollama import ollama
from ragfmk.elements.wrappers.prompt import prompt
from ragfmk.utils.trace import trace
from ragfmk.elements.embeddings.embeddings import embeddings
from ragfmk.elements.embeddings.stEmbeddings import stEmbeddings
from ragfmk.elements.wrappers.chunks import chunks
from ragfmk.interfaces.IRag import IRag
import ragfmk.utils.CONST as C

import requests
import os
import time

class rag(IRag):
    def __init__(self):
        self.__trace = trace()
        self.__trace.start()

    def initSearchEngine(self):
        # No search engine for the high level class
        pass
    def processSearch(self, k, vPrompt):
        # No search engine for the high level class
        pass
    def addEmbeddings(self, vChunks):
        # No search engine for the high level class
        pass

    def __fmtMsgForLog(self, message, limit = C.TRACE_MSG_LENGTH):
        """ Format a message for logging
        Args:
            message (str): log message
            limit (int, optional): message max length. Defaults to C.TRACE_MSG_LENGTH.
        Returns:
            formatted message: _description_
        """
        logMsg = message.replace("\n", " ")
        dots = ""
        if (len(message) > limit):
            dots = " ..."
        logMsg = logMsg[:limit] + dots
        return logMsg

    @property
    def trace(self):
        return self.__trace

    def addMilestone(self, name, description, *others):
        self.trace.add(name, description, others)
        self.trace.addlog("INFO", "Step {} -> {}".format(name, self.__fmtMsgForLog(description)))

    def readTXT(self, txtfile):
        """ Reads a txt file
        Args:
            txtfile (str): text file path
        Returns:
            str: text read
        """
        try:
            # Read and parse a pdf file
            self.trace.addlog("INFO", "Read TXT file {} by using mode ...".format(txtfile))
            doc = document()
            doc.load(txtfile)
            if (len(doc.content) <= 0):
                raise Exception("Error while reading the TXT document")
            self.addMilestone("PDF2TXT", "TXT file successfully loaded. Text length : {}".format(len(doc.content)))
            return doc
        except Exception as e:
            self.trace.addlog("ERROR", "Error while reading the TXT file: {}".format(str(e)))
            return document()

    def readPDF(self, pdffile, method = C.READER_VALPYPDF):
        """ Reads a pdf file and converts it to Text
        Args:
            pdffile (str): pdf file path
            method (str, optional): Type of conversion. Defaults to C.READER_VALPYPDF.
        Returns:
            str: text converted
        """
        try:
            # Read and parse a pdf file
            self.trace.addlog("INFO", "Read PDF file {} by using mode {}...".format(pdffile, method))
            pdf = document()
            if (method == C.READER_VALPYPDF):
                pdf.pyMuPDFParseDocument(pdffile)
            else:
                pdf.llamaParseDocument(pdffile)
            if (len(pdf.content) <= 0):
                raise Exception("Error while converting the PDF document to text")
            self.addMilestone("PDF2TXT", "PDF converted to TEXT successfully. Text length : {}".format(len(pdf.content)))
            return pdf
        except Exception as e:
            self.trace.addlog("ERROR", "Error while reading the PDF file: {}".format(str(e)))
            return document()
            
    def charChunk(self, doc, separator, chunk_size, chunk_overlap) -> chunks:
        """ Document character chunking process
        Args:
            doc (elements.document): Text / document to chunk
            separator (str): Chunks separator
            chunk_size (str): chunk size
            chunk_overlap (str): chunk overlap
        Returns:
            chunks: chunks object
        """
        try:
            self.trace.addlog("INFO", "Character Chunking document processing ...")
            cks =  doc.characterChunk(separator, chunk_size, chunk_overlap)
            if (cks == None):
                raise Exception("Error while chunking the document")
            self.addMilestone("CHUNKING","Document (character) chunked successfully, Number of chunks : {}".format(cks.size), cks.size)
            return cks
        except Exception as e:
            self.trace.addlog("ERROR", "Error while chunking the document: {}".format(str(e)))
            return None

    def semChunk(self, doc) -> chunks:
        """ Document semantic chunking process
        Args:
            doc (elements.document): Text / document to chunk
        Returns:
            int: number of chunks
            list: List of chunks / JSON format -> {'chunks': ['Transcript of ...', ...] }
        """
        try:
            self.trace.addlog("INFO", "Semantic Chunking document processing ...")
            cks =  doc.semanticChunk()
            if (cks == None):
                raise Exception("Error while chunking the document")
            self.addMilestone("CHUNKING","Document (character) chunked successfully, Number of chunks : {}".format(cks.size), cks.size)
            return cks
        except Exception as e:
            self.trace.addlog("ERROR", "Error while chunking the document: {}".format(str(e)))
            return None
        
    def buildPrompt(self, question, nr) -> str:
        """ Build smart prompt (for RAG)
        Args:
            question (str): initial question
            nr (nearest object): list of the nearest / most similar chunks
        Returns:
            str: new prompt
        """
        try:
            self.trace.addlog("INFO", "Building RAG prompt ...")
            myPrompt = prompt(question, nr)
            customPrompt = myPrompt.build()
            if (len(customPrompt) == 0):
                raise Exception("Error while creating the prompt")
            self.addMilestone("PROMPT", "Prompt built successfully", customPrompt)
            return customPrompt
        except Exception as e:
            self.trace.addlog("ERROR", "Error while building the LLM prompt {}".format(str(e)))
            return ""

    def promptLLM(self, question, urlOllama, model, temperature, contextwindow=C.OLLAMA_DEFAULT_CTXWIN):
        """ send a prompt to the LLM
        Args:
            question (str): prompt
            urlOllama (str): Ollama URL
            model (str): Ollama Model
            temperature (str): Ollama Model LLM Temperature
        Returns:
            str: LLM response
        """
        try:
            self.trace.addlog("INFO", "Send the prompt to the LLM ...")
            myllm = ollama(urlOllama, model, temperature, contextwindow)
            resp = myllm.prompt(question)
            try:
                token_used = resp["prompt_eval_count"]
            except:
                token_used = 0
            self.addMilestone("LLMPT", "LLM Reponse\n {}\n".format(resp["response"]))
            return resp["response"], token_used
        except Exception as e:
            self.trace.addlog("ERROR", "Error while prompting the LLM {}".format(str(e)))
            return "", 0
    
    def createEmbeddings(self, cks, embds = None) -> embeddings:
        """ create embeddings for a list of chunks
        Args:
            cks (chunks): Chunks object (list of texts)
            embds (embeddings): embeddings object Factory by default uses the class stEmbeddings (Sentence Transformer)
        Returns:
            json: data and embeddings
        """
        try:
            if (embds == None):
                embds = stEmbeddings()
            self.trace.addlog("INFO", "Create embeddings for list of texts/chunks ...")
            if (not embds.create(cks)):
                raise Exception("Error while creating the chunks embeddings")
            self.addMilestone("DOCEMBEDDGS", "Embeddings created from chunks successfully")
            return embds
        except Exception as e:
            self.trace.addlog("ERROR", "Error while creating the list of texts/chunks embeddings {}".format(str(e)))
            return None
        
    def HallucinationDetector(self, response1, response2) -> float:
        """ The HHEM model is an open source model, created by Vectara, for detecting hallucinations in LLMs. 
            It is particularly useful in the context of building retrieval-augmented-generation (RAG) applications where 
            a set of facts is summarized by an LLM, but the model can also be used in other contexts.
            Cf. https://huggingface.co/vectara/hallucination_evaluation_model
            Note: the environment variable HUGGINGFACE_API_KEY must be set with a valid HF token
        Args:
            response1 (_type_): Response 1 to check
            response2 (_type_): Response 2 to check
        Returns:
            float: return the confidence score (under 0,5 it's probably an hallucination)
        """
        try:
            # Get the API Hugging Face key first
            try:
                huggingFaceKey = os.environ[C.HUGGINGFACE_API_KEY]
            except:
                raise Exception ("The {} environment variable needs to be defined to use Hugging Face.".format(C.HUGGINGFACE_API_KEY))

            headers = {"Authorization": "Bearer " + huggingFaceKey}
            payload = { "inputs": response1 + "[SEP]" + response2 }
            
            # May need some time to load the model especially the first time
            iteration = 1
            while True:
                response = requests.post(C.HHEM_HF_MODEL, headers=headers, json=payload)
                if response.status_code == 200:
                    break
                time.sleep(C.HF_API_WAITSEC)
                if (iteration >= C.HF_ITERATION_MAX):
                    raise Exception ("Llamaindex seems not responsive or not responsive enough, please retry again.")
                iteration += 1
            
            hallucinationScore = response.json()[0][0]["score"]
            return float(hallucinationScore)
        except Exception as e:
            self.trace.addlog("ERROR", "Error while checking hallucinations {}".format(str(e)))
            return None
            