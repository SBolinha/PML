# PML - Python Markup Language

## Purpose: render XML files more readible

### Introduction:

Lengty HTML and XML documents with many embedded elements can be very difficult to read.

Via the XML DOM model, all elements and attributes can be translated into Nodes and subsequently be queried.
However, this quite elaborate process does not help to quickly consult a well-formed XML document.

The Python language is a very good example of reducing/removing delimiters.
This makes the underlying structure clearer and easier to interpret.

Following the Python language example, it is set out here to simplify the display of structured and well-formed XML documents.
In particular for well-formed XML documents, the display can be simplified by removing unnecessary delimiters.

The present simplification includes:
* nodes and subnodes and their attributes are presented by means of indentation
* the closing tag for an element is suppressed and replaced by out-dentation (just as in Python)
* the structure within an attribute is remained intact: XML does not consider this part of the DOM structure, but simply as content

### Usage:

```
xml2pml(<required: XML content>,
        [optional: default indentation],
        [optional: indentation string],
        [optional: element tag indicator],
        [optiontal: attribute tag indicator])
```

The function requires the following input:
* [required] a complete or partial content-blob from a well-formed XML document
* [optional] in following sequence:
* * indentation {default = 0}
  * indentation string {default = '    '}
  * element tag indicator, can be set to empty string '' {default = '§.'}
  * attribute tag indicator, can be set to empty string '' {default = '@.'} 

<u>Notes:</u>
* The ```§.``` element tag indicator and the ```@.``` attribute tag indicator are set as default, since these would allow to reverse engineer the original XML structure
* When concise readibilty is the only objective: The element tag indicator or the attribute tag indicator can be set to empty (''). Also the indentation string can be set to less spaces.
* Recommendation: do not use ```<``` or ```>``` characters as element tag indicator or attribute tag indicator, the <pml>...</pml> blob can then even be included into a XML file.

### Example of use:

```
myxml = {...str content of an XML document...}

print(xml2pml(myxml))
```

### Further examples:

#### 1. Snippet of an XML file:
```
start<p 
id="main" cover='I like this'>Hello<b>bold</b>text<br/><table test='tryout:"true in value, index=300"'/>do
 that<css namespace="unknown test:'true value=110'" onclick="do this"/><h1 value=3>Heading</h1>test</p>end
```

Result of ```xml2pml``` on this snippet, using default settings:

```
                <pml>start
                §.p
                    @.id="main"
                    @.cover='I like this'
                    Hello
                    §.b
                        bold
                    text
                    §.br
                    §.table
                        @.test='tryout:"true in value, index=300"'
                    do
                     that
                    §.css
                        @.namespace="unknown test:'true value=110'"
                        @.onclick="do this"
                    §.h1
                        @.value=3
                        Heading
                    test
                end</pml>
```


