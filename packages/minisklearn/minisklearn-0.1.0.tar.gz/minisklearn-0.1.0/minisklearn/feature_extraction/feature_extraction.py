import re
from base import Transformer
from scipy.sparse import csr_matrix
from collections import defaultdict

class SimpleCountVectorizer(Transformer):
    """
    A simplified version of CountVectorizer to convert a collection of text documents into a matrix of token counts.
    """
    
    def __init__(self):
        """
        Initializes the SimpleCountVectorizer with an empty vocabulary.
        """
        self.vocabulary_ = {}

    def _build_vocab_and_count(self, documents, use_fixed_vocabulary):
        if not use_fixed_vocabulary:
            self.vocabulary_ = {}
            vocab_index = 0
        vocabulary = self.vocabulary_
        values, column_indices, row_ptr = [], [], [0]

        for document in documents:
            feature_counts = defaultdict(int)

            token_pattern = re.compile(r'\b[a-zA-Z]{2,}\b')
            tokens = token_pattern.findall(document.lower())
            for token in tokens:
                if token not in vocabulary and not use_fixed_vocabulary:
                    vocabulary[token] = vocab_index
                    vocab_index += 1
                if token in vocabulary:
                    token_index = vocabulary[token]
                    feature_counts[token_index] += 1

            values.extend(feature_counts.values())
            column_indices.extend(feature_counts.keys())
            row_ptr.append(len(column_indices))

        return vocabulary, csr_matrix((values, column_indices, row_ptr), shape=(len(row_ptr) - 1, len(vocabulary)))


    def fit(self, documents):
        """
        Learn a vocabulary dictionary of all tokens in the raw documents.

        Parameters:
        documents (list of str): An iterable which yields either str, unicode or file objects.
        
        Returns:
        SimpleCountVectorizer: The instance itself.
        """
        _, _ = self._build_vocab_and_count(documents, use_fixed_vocabulary=False)
        self.vocabulary_ = {term: idx for idx, (term, _) in enumerate(sorted(self.vocabulary_.items()))}
        return self

    def transform(self, documents):
        """
        Transform documents to document-term matrix using the learned vocabulary.

        Parameters:
        documents (list of str): An iterable which yields either str, unicode or file objects.
        
        Returns:
        csr_matrix: Document-term matrix.
        """
        _, doc_term_matrix = self._build_vocab_and_count(documents, use_fixed_vocabulary=True)
        return doc_term_matrix

    def get_feature_names(self):
        """
        Get a list of feature names, ordered by their indices in the vocabulary.

        Returns:
        list: Sorted list of feature names in the vocabulary.
        """
        return sorted(self.vocabulary_.keys())
