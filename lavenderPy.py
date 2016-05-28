from __future__ import print_function

# Lists with words that frequently follow possesive pronouns. 
_conjunctions = set(["after", "although", "and", "as", "because", "before", "but", "by", "even", "in", "lest", "once", "only", "or", "provided", "since", "so", "than", "that", "though", "till", "unless", "until", "when", "whenever", "where", "wherever", "while"])
_prepositions = set([ "aboard", "about", "above","across", "after", "against", "along", "amid", "among", "anti", "around", "as", "at", "before", "behind", "below", "beneath", "beside", "besides", "between", "beyond", "but", "by", "concerning", "considering", "despite", "down", "during", "except", "excepting", "excluding", "following", "for", "from", "in", "inside", "into", "like", "minus", "near", "of", "off", "on", "onto", "opposite", "outside", "over", "past", "per", "plus", "regarding", "round", "save", "since", "than", "through", "to", "toward", "towards", "under", "underneath", "unlike", "until", "up", "upon", "versus", "via", "with", "within", "without" ])
_punc = list(".,?!:;)")

_mapping = [
        (" she ", " ze "),
        (" he ", " ze "),
        (" him ", " hir "),
        (" her ", " hir "),
        #(" his ", " hir "),
        #(" his ", " hirs "),
        (" hers ", " hirs "),
        (" himself ", " hirself "),
        (" herself ", " hirself "),
        (" s/he ", " ze "),
        (" (s)he ", " ze "),
        (" he or she ", " ze "),
        (" she or he ", " ze "),
    ]

_cap = lambda x : " " + x[1].upper() + x[2:]
_mapping = _mapping + [ (_cap(a), _cap(b)) for a, b in _mapping ] 
_mappingSimple = []
for k, v in _mapping:
	for p in _punc:
	    _mappingSimple.append((k, v))
	    _mappingSimple.append((k[:-1] + p, v[:-1] + p))

_followsHirs = set(list(_conjunctions) + list(_prepositions) + _punc)
_hisPunc = set(["his" + p for p in _punc] + ["His" + p for p in _punc])


def _replaceHis(text):
    """
        This function replaces `his' with either `hir' or `hirs', depending
        on the part-of-speech. This is done heuristically to avoid dependencies,
        but a pos-tagger would improve the accuracy. For now, the vast majority 
        would is handled correclty like this.
    """
    tokens = text.split(" ")
    # Iterate over tokens while looking ahead one token.
    for i in range(len(tokens)-1):
        if tokens[i] in _hisPunc:
            hirs = "hirs" if tokens[i][0] == "h" else "Hirs"
            tokens[i] = hirs + tokens[i][-1]
        elif tokens[i] in ["his", "His"] and tokens[i+1] in _followsHirs:
            hirs = "hirs" if tokens[i][0] == "h" else "Hirs"
            tokens[i] = hirs
        elif tokens[i] in ["his", "His"]:
            hir = "hir" if tokens[i][0] == "h" else "Hir"
            tokens[i] = hir
    # Check last token.
    last = -1
    if tokens[last] in _hisPunc:
        hirs = "hirs" if tokens[last][0] == "h" else "Hirs"
        tokens[last] = hirs + tokens[last][-1]
    if tokens[last] in ["his", "His"]:
        hirs = "hirs" if tokens[last][0] == "h" else "Hirs"
        tokens[last] = hirs
    return " ".join(tokens)
          
def lavenderize(text):
    """
        Takes an english text string and makes all pronouns gender neutral.
    """
    text = " " + text + " "
    for k, v in _mappingSimple:
        text = text.replace(k,v)
    return _replaceHis(text)[1:-1]

if __name__=="__main__":
    example = "S/he was a big woman who enjoyed going out with him. He, however, was deeply in love with her." 
    print("Original:")
    print(example)
    print("Lavendized:")
    print(lavenderize(example))
