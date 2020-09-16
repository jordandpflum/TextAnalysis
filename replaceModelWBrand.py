

def replaceModelWBrand(tokens, wordBrandCSV):
    """
    Replace Model Occurance with Brand
    :param tokens: list of all important words in comments
    :param wordBrandCSV: CSV of word-brand association
    :return: a list of allBrands mentioned in the comments
    """
    brandWordAssociation = pd.read_csv('car models and brands.csv')
    brandWords = brandWordAssociation['Model']
    brandWordAssociation.set_index('Model')
    brandWordAssociation = brandWordAssociation.to_dict()
    for i in range(len(tokens)):
        word = tokens[i].lower()
        if word in brandWords:
            tokens[i] = brandWordAssociation[word]
    return tokens









