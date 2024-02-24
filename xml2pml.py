def xml2pml(xml, otll=0, tab='    ', tag='§.', att='@.', KeepCR=True):
#   otll = 0 # outer tag level
#   tab = '    ' # default basis for tabulation
#   tag = '§.' # default element tag indicator
#   att = '@.' # default attribute tag indicator
#   KeepCR = True # by default transfer <CR> from the source XML
    atln = -1 # attribute tag length
    tlln = 0 # tag label length
    squot = False # inside single quoted  content
    dquot = False # inside double quoted content
    intag = False # inside tag
    ttype = '' # tag content type
    pl = '' # previous character
    l = '' # the current character being processed

    pml = ''
    for l in xml:
        if l == '<':
            intag = True
            ttype = '' # reset tag type
            tlln = 0
            atln = -1
            pml += '\n' + tab * otll
        elif l == '>':
            intag = False
            # Handle the indentation and <CR> after the tag
            if ttype == '/':
                otll = max(otll-1, 0) # hand brake procedure to avoid excessive outdentation
                pml += '\n' + tab * otll
            elif pl == '/': # self-closing tag
                pml += '\n' + tab * otll
            elif ttype in ['?', '!']: # treat as self-closing tag
                pml += '\n' + tab * otll
            else:
                otll +=1
                pml += '\n' + tab * otll
        else: # implicitly: the < and > symbols are not sent to output, the rest is passed through
            if intag:
                if tlln == 0: # first character of the element tag
                    if l in ['/', '?', '!']:
                        ttype = l
                    else:
                        ttype = '<' # regular opening tag
                        pml += tag # add the element tag identifier to allow reverse engineering
                    tlln = 1

                if ttype == '/':
                    pass
                elif l == '/' and not(squot) and not(dquot) and ttype=='<': #  do not process the slash
                    pass
                elif l == '\n': # <CR> in elements will be removed
                    pass
                elif l == ' ' and not(squot) and not(dquot) and ttype=='<': # potential for attributes
                    l = '' # remove spaces
                    atln = 0
                elif atln == 0 and ttype=='<':
                    pml += '\n' + tab * (otll + 1)
                    atln += 1
                    pml += att + l                    
                    if l=="'" and not(dquot):
                        squot = not(squot)
                    elif l=='"' and not(squot):
                        dquot = not(dquot)
                elif atln > 0 and ttype=='<':
                    atln += 1
                    pml += l
                    if l=="'" and not(dquot):
                        squot = not(squot)
                    elif l=='"' and not(squot):
                        dquot = not(dquot)
                else: # add the to the element tag label
                    tlln += 1
                    pml += l
            else: # just content, but may depend on tag type
                if l == '\n': # add left tabulation
                    pml += '\n' + tab * otll
                else:
                    pml += l
        pl = l

    if not KeepCR:
        tmp = ''
        for line in pml.split('\n'):
            if len(''.join(line.split()))>0: # only keep lines with text content
                tmp += line + '\n'
        pml=tmp
    return '<pml>' + pml + '</pml>'
