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

### What does it do?

#### The XML content is processed as follows:
* strip all XML formatting from the elements
* remove all closing tags, these are implicit
* print every XML element on a new line, proceeded by an element tag indicator (default ```'§.'```)
* print every attribute of an XML document indented on a new line, proceeded by an attribute tag indicator (default ```'@.'```)
* print all text content within an element indented on a new line
* keep original format for ```'<[CDATA[]]>'``` and ```'<?xml namespace="..">'``` type of elements

#### The present simplification includes:
* nodes and subnodes and their attributes are presented by means of indentation
* the closing tag for an element is suppressed and replaced by out-dentation (just as in Python)
* the structure within an attribute is remained intact: XML does not consider this part of the DOM structure, but simply as content

### Usage:

```
xml2pml(<required: XML content>,
        [optional: default indentation],
        [optional: indentation string],
        [optional: element tag indicator],
        [optional: attribute tag indicator],
        [optional: KeepCR set to False])
```

The function requires the following input:
* [required] a complete or partial content-blob from a well-formed XML document
* [optional] in following sequence:
* * indentation {default = 0}
  * indentation string {default = ```'    '```}
  * element tag indicator, can be set to empty string ```''``` {default = ```'§.'```}
  * attribute tag indicator, can be set to empty string ```''``` {default = ```'@.'```}
  * KeepCR boolean, can be set to ```'False'``` to avoid the source ```<CR>``` carriage-returns (the ```'\n'``` operator) into the PML {default = ```True```}

<u>Notes:</u>
* The ```§.``` element tag indicator and the ```@.``` attribute tag indicator are set as default, since these would allow to reverse engineer the original XML structure
* When concise readibilty is the only objective: The element tag indicator or the attribute tag indicator can be set to empty (''). Also the indentation string can be set to less spaces.
* Recommendation: do not use ```'<'``` or ```'>'``` characters as element tag indicator or attribute tag indicator, the ```'<pml>...</pml>'``` blob can then even be included into a XML file.

### Example of use:

```
myxml = {...str content of an XML document...}

print(xml2pml(myxml))
```

### Examples:

#### 1. Snippet of an XML file:
```
start<p 
id="main" cover='I like this'>Hello<b>bold</b>text<br/><table test='tryout:"true in value, index=300"'/>do
 that<css namespace="unknown test:'true value=110'" onclick="do this"/><h1 value=3>Heading</h1>test</p>end
```

Source content in Python:
```
myxml = 'start<p \nid="main" cover=' + "'I like this'" + '>Hello<b>bold</b>text<br/><table test=' + "'tryout:" + \
    '"true in value, index=300"' + "'" + '/>do\n that<css namespace="unknown test:' + "'true value=110'" + '" onclick="do this"/><h1 value=3>Heading</h1>test</p>end'
```

Calling XML2PML in Python:
```
mypml = xml2pml(myxml, 4)
print(mypml)
```

Result of ```xml2pml``` on this snippet, using 4x indentation and otherwise default PML settings:

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

#### 2. Snippet of a car configuration file:

Clearly difficult to interpret:
```
myxml = """<parameter group="GROUP_CCF_TPMS_SYSTEM" name="PARAM_CCF_TPMS_TDWS" scope="base">\
<group_name><text><tm>Tire pressure monitoring</tm></text></group_name>\
<param_name><text><tm>Tire pressure monitor system</tm></text></param_name>\
<parameter_active><source name="AS_BUILT"><value option="TPMS">\
<text><tm id="@J_I_TPM_FITTED">Tire pressure monitor system is fitted.</tm></text>\
<data formatted="Tire pressure monitor system is fitted." type="ENUM">0x01</data>\
</value></source></parameter_active><parameter_mismatch/><parameter_not_available/></parameter>"""
```

Calling XML2PML in Python:
```
mypml = xml2pml(myxml, 0, '  ', '', '') # to minimise the output
print(mypml)
```

Result:
```
<pml>
parameter
  group="GROUP_CCF_TPMS_SYSTEM"
  name="PARAM_CCF_TPMS_TDWS"
  scope="base"
  group_name
    text
      tm
        Tire pressure monitoring
  param_name
    text
      tm
        Tire pressure monitor system
  parameter_active
    source
      name="AS_BUILT"
      value
        option="TPMS"
        text
          tm
            id="@J_I_TPM_FITTED"
            Tire pressure monitor system is fitted.
        data
          formatted="Tire pressure monitor system is fitted."
          type="ENUM"
          0x01
  parameter_mismatch
  parameter_not_available</pml>
```
