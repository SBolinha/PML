def xml2pml(xml, otll=0, tab='    ', tag='§.', att='@.', KeepCR=True):
#   otll = 0 # outer tag level
#   tab = '    ' # default basis for tabulation
#   tag = '§.' # default element tag indicator
#   att = '@.' # default attribute tag indicator
#   KeepCR = True # by default transfer <CR> from the source XML
    itll = 0 # inner tag level
    atln = -1 # attribute length
    tlln = 0 # tag label length
    nclt = True # non-closing tag
    squot = False
    dquot = False

    pml = tab*otll          
    for l in xml:
        if l == '>':
            itll = 0
            atln = -1
            if nclt:
                otll += 1
            else:
                otll -= 1
            nclt = True
        elif l == '/':
            if tlln > 0:
                otll -=1 # a self-closing tag, compensate for outer tag level increment later
            else: # a closing tag
                tlln = 1 # just a default value
                nclt = False
        elif l == '<':
            itll = 1
            tlln = 0
        else:
            if itll>0:
                if nclt:
                    if l == ' ' and not(squot or dquot): # remove the <space> in the non-attribute part of the tag, detection of attributes is possible
                        atln=0
                        itll = 1 # reset to default in tag level
                        l = ''
                    elif l == '\n': # remove the <space> or the <cr> in the tag, detection of attributes is possible
                        atln=0
                        itll = 1 # reset to default in tag level
                        l = ''
                    elif l == '"' and not(squot): # double quote level can only be actuated if no single quote level is active
                        dquot = not(dquot)
                    elif l == "'" and not(dquot): # sing;e quote level can only be actuated if no double quote level is active
                        squot = not(squot)
                    else: # tag or attribute character detected
                        if atln<0: # attribute tag is not yet possible, must be a tag
                            if tlln == 0:
                                pml += '\n' + tab*otll + tag            
                            tlln += 1
                        elif atln==0: # first character of the attribute tag, following <space> or <crlf>
                            itll +=1
                            atln += 1
                            pml += '\n' + tab*(otll + itll - 1) + att          
                        else:
                            atln +=1
                    pml += l          
                else:
                    pass # nothing to be done for a closing tag
            else: # outside an element
                if tlln>0: # coming just out of an element
                    if nclt:
                        pml += '\n' + tab*otll         
                    tlln = 0
                if l == '\n':
                    pml += '\n' + tab*otll
                else:
                    pml += l
    tmp = ''
    if KeepCR == False:
        for line in pml.split('\n'):
            if len(''.join(line.split()))>0: # only keep lines with text content
                tmp += line + '\n'
        pml=tmp
    return '<pml>' + pml + '</pml>'
