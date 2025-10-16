import html

class Encoding:

    @staticmethod
    def decode(encoded:str):
        ''' Decode html encoded string
        '''
        return html.unescape(encoded)
    
    @staticmethod
    def encode(decoded:str):
        '''Encode provided string with html encoding'''
        return html.escape(decoded)