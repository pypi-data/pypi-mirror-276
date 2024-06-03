import os
import shutil
import tempfile

from time import sleep
from whoosh import fields
from whoosh import index
from whoosh.query import And
from whoosh.query import Or
from whoosh.query import Term
from whoosh.qparser import QueryParser
from whoosh.index import LockError

class WhooshSearch(object):
    """full-text search"""

    def __init__(self, whoosh_index=None):
        """
        - whoosh_index : whoosh index directory
        """
        self.schema = fields.Schema(name=fields.ID(unique=True, stored=True),
                                    description=fields.TEXT)
        self.keywords = set([])
        self.tempdir = False
        if whoosh_index is None:
            whoosh_index = tempfile.mkdtemp()
            self.tempdir = True
        if not os.path.exists(whoosh_index):
            os.makedirs(whoosh_index)
        self.index = whoosh_index
        self.ix = index.create_in(self.index, self.schema)

    def update(self, name, description, **kw):
        """update a document"""

        # forgivingly get the writer
        timeout = 3. # seconds
        ctr = 0.
        incr = 0.2
        while ctr < timeout:
            try:
                writer = self.ix.writer()
                break
            except LockError:
                ctr += incr
                sleep(incr)
        else:
            raise

        # add keywords
        for key in kw:
            if key not in self.keywords:
                writer.add_field(key, fields.KEYWORD)
                self.keywords.add(key)
            if not isinstance(kw[key], str):
                kw[key] = ' '.join(kw[key])
            kw[key] = str(kw[key])

        writer.update_document(name=name, description=description, **kw)
        writer.commit()

    def delete(self, name):
        """delete a document of a given name"""
        writer = self.ix.writer()
        writer.delete_by_term('name', name)
        writer.commit()

    def __call__(self, query):
        """search"""
        query_parser = QueryParser("description", schema=self.ix.schema)
        myquery = query_parser.parse(query)


        # New code: too permissive
        excluded = set(['AND', 'OR', 'NOT'])
        terms = [i for i in query.split() if i not in excluded]
        extendedquery = And([Or([myquery] + [Term('description', term), Term('name', term)] +
                                [Term(field, term) for field in self.keywords]) for term in terms])

        # perform the search
        searcher = self.ix.searcher()
        return [i['name'] for i in searcher.search(extendedquery, limit=None)]

    def __del__(self):
        if self.tempdir:
            # delete the temporary directory, if present
            shutil.rmtree(self.index)
