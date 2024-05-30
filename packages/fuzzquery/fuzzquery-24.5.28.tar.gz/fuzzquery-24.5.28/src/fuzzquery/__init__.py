"""A lightweight package for fuzzy word/phrase searches in a body of text, using a very simple token system.

project: https://pypi.org/project/fuzzquery/

version: 24.5.28

author: OysterShucker

tokens:
 tokens have up to 3 parts:
 - "x" = a number of characters or words to find. this number by default is considered a range: 0 to `x`
 - "=" = exactly `x`, instead of a range
 - "w" = signifies the token should match words
 
token examples:
 - "{5}"  : from 0 to 5 non-whitespace characters
 - "{=3}" : exactly 3 non-whitespace characters
 - "{5w}" : 0 to 5 words
 - "{=3w}": exactly 3 words
    
query examples:
 - "home{5}"         : home, homer, homely, homeward, homestead
 - "bomb{=2}"        : bomber, bombed
 - "bomb{=2}{3}"     : bomber, bombed, bombers, bombastic
 - "thou {=2w} kill" : thou shalt not kill
 - "{2}ward{=2}"     : warden, awarded, rewarded
 * "{4}{=3}-{=4}"    : 504-525-5555, 867-5309, more-or-less
 
 * searches this broad are bound to return some unwanted results
"""
import re
from typing import Iterator

__all__ = 'finditer', 'findany', 'iterall'

FLAGS = None, re.I
TOKEN = re.compile(r'(\{={0,1}\d+[cw]{0,1}\})')

FORMATS = {
    'char' : r'(?:\S){{{start},{stop}}}',
    'word' : r'(?:\S+?(?:\s+?|$)){{{start},{stop}}}',
}

# convert query to expression
def __expr(query:str, group:bool=True) -> str:

    # convert term segment to expression
    def subexpr(segment:str, _start:int=0, _stop:int=0, _type:str='explicit') -> str:
        if TOKEN.fullmatch(segment) is not None:
            _type  = ('char', 'word')['w' in segment]
            _stop  = int(''.join(filter(str.isdigit, segment)) or 0)
            _start = _stop * ('=' in segment)

        return FORMATS.get(_type, re.escape(segment)).format(start=_start, stop=_stop)
    
    # term segments
    segmap = filter(None, map(TOKEN.split, query.split(' ')))
    
    # generator of terms from processed term segments
    terms = (r''.join(map(subexpr, filter(None, segments))) for segments in segmap)
    
    # join terms with conditional spacing
    expr  = r'(?:(?<=\s)|\s)+?'.join(terms)
    
    # create final expression
    return f'{"("*group}{expr}{")"*group}'
   
# execute final expression on text
def __exec(expr:str, text:str, skip:None|list|tuple|set=None, ci:bool=False) -> Iterator:
    skip = skip or []
    
    for match in re.finditer(expr, text, flags=FLAGS[ci]):
        result = match.group('result')
        
        # determine if result should be skipped
        for item in skip:
            if item in result: break
        else:
            yield match.span(), result

def finditer(text:str, query:str, **kwargs) -> Iterator:
    """Format query into an expression and yield matches
    
     - text    : str
       the text to be searched
         
     - query   : str
       str of term(s) to search for
         
     ** skip   : list|tuple|set, optional
       words and/or characters that trigger a skip when found in a result
         
     ** ci     : bool, optional
       case insensitive matching  
         
     return tuple of query results (`span`, `results`)
    """
    expr = fr'\b(?P<result>{__expr(query, False)})\b'
    
    for span, result in __exec(expr, text, **kwargs):
        yield span, result
          
def findany(text:str, queries:list|tuple|set, **kwargs) -> Iterator:
    """Format and OR queries into a singular expression and yield matches
    
     - text    : str
       the text to be searched
       
     - queries : list|tuple|set
       Iterable of search terms
       
     ** skip   : list|tuple|set, optional
       words and/or characters that trigger a skip when found in a result
       
     ** ci     : bool, optional
       case insensitive matching  
     
     return tuple of query results (`span`, `results`)
    """
    expr = r'|'.join(map(__expr, queries))
    expr = fr'\b(?P<result>{expr})\b'
    
    for span, result in __exec(expr, text, **kwargs):
        yield span, result

def iterall(text:str, queries:list|tuple|set, **kwargs) -> Iterator: 
    """Yield from multiple consecutive queries
     
     - text    : str
       the text to be searched
       
     - queries : list|tuple|set
       Iterable of search terms
       
     ** skip   : list|tuple|set, optional
       words and/or characters that trigger a skip when found in a result
       
     ** ci     : bool, optional
       case insensitive matching  
     
     return tuple of query results (`query`, `span`, `results`)
    """
    for query in queries:
        q = query
            
        for span, match in finditer(text, query, **kwargs):
            yield q, span, match
            q = None # only yield `query` on first match

