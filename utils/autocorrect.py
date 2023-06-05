from gingerit.gingerit import GingerIt


def autocorrect(text: str):
    parser = GingerIt()
    corrected = ''
    
    splitted = text.split("\n\n")
    
    for paragraph in splitted:
        if len(paragraph) > 500:
            splitted_paragraph = paragraph.split(". ")
            
            corrected = corrected + "\n\n"
            
            for sentence in splitted_paragraph:
                corrected_sentence = parser.parse(sentence)
                corrected = corrected + ". " + corrected_sentence['result']
        else: 
            corrected_section = parser.parse(paragraph)
            corrected = corrected + "\n\n" +  corrected_section['result']
        
        
    return corrected