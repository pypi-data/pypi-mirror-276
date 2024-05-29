# uztagger

https://pypi.org/project/uztagger <br>
https://github.com/UlugbekSalaev/uztagger

uztagger is focused to make tagging sentence with morphological Part of Speech (POS) tagset of Uzbek word based on morphemes and limited number of lexicon. The tool includes list of POS tagset, tagging method. 
It is created as a python library and uploaded to [PyPI](https://pypi.org/). It is simply easy to use in your python project or other programming language projects via the API. 

## About project
The tool is focused to make tagging sentence with morphological Part of Speech (POS) tagset of Uzbek word based on morphemes. The tool includes list of POS tagset, tagging method.

## Quick links

- [Github](https://github.com/UlugbekSalaev/uztagger)
- [PyPI](https://pypi.org/project/uztagger/)
- [Web-UI](https://nlp.urdu.uz/?menu=uztagger)

## Demo

You can use [web interface](http://nlp.urdu.uz/?menu=uztagger).

## Features

- Tagging 
- POS tag list
- Help function

## Usage

Three options to run uztagger:

- pip
- API 
- Web interface

### pip installation

To install uztagger, simply run:

```code
pip install uztagger
```

After installation, use in python like following:
```yml
# import the library
from uztagger import Tagger
# create an object 
tagger = Tagger()
# call tagging method
tagger.pos_tag('Bizlar bugun maktabga bormoqchimiz.')
# output
[('Bizlar','NOUN'),('bugun', 'NOUN'), ('maktabga', 'NOUN'), ('bormoqchimiz', 'VERB'), ('.', 'PUNC')]
```

### API
API configurations: 
 - Method: `GET`
 - Response type: `string`
 - URL: `https://nlp.urdu.uz:8080/uztagger/pos_tag`
   - Parameters: `text:string`
 - Sample Request: `https://nlp.urdu.uz:8080/uztagger/pos_tag?text=Ular%20maktabga%20borayaptilar.`
 - Sample output: `[("Ular","NOUN"),("maktabga",""),("borayaptilar",""),(".","PUNC")]`

### Web-UI

The web interface created to use easily the library:
You can use web interface [here](http://nlp.urdu.uz/?page=uztagger).

![Demo image](src/uztagger/web-interface-ui.png)

### POS tag list
Tagger using following options as POS tag:<br>
    `NOUN`  Noun {Ot}<br>
    `VERB`  Verb {Fe'l}<br>
    `ADJ `  Adjective {Sifat}<br>
    `NUM `  Numeric {Son}<br>
    `ADV `  Adverb {Ravish}<br>
    `PRN `  Pronoun {Olmosh}<br>
    `CNJ `  Conjunction {Bog'lovchi}<br>
    `ADP `  Adposition {Ko'makchi}<br>
    `PRT `  Particle {Yuklama}<br>
    `INTJ`  Interjection {Undov}<br>
    `MOD `  Modal {Modal}<br>
    `IMIT`  Imitation {Taqlid}<br>
    `AUX `  Auxiliary verb {Yordamchi fe'l}<br>
    `PPN `  Proper noun {Atoqli ot}<br>
    `PUNC`  Punctuation {Tinish belgi}<br>
    `SYM `  Symbol {Belgi}<br>

### Result Explaining

The method ```pos_tag``` returns list, that an item of the list contain tuples for each token of the text with following format: ```(token, pos)```, for POS tag list, see <i>POS Tag List</i> section on above.  
#### Result from `tagger` method
`[('Bizlar','NOUN'),('bugun', 'NOUN'), ('maktabga', 'NOUN'), ('bormoqchimiz', 'VERB'), ('.', 'PUNC')]`

## Documentation

See [here](https://github.com/UlugbekSalaev/uztagger).

## Citation

```tex
@misc{uztagger,
  title={{uztagger}: Morphological Part of Speech Tagger Tool for Uzbek},
  url={https://github.com/UlugbekSalaev/uztagger},
  note={Software available from https://github.com/UlugbekSalaev/uztagger},
  author={
    Ulugbek Salaev},
  year={2022},
}
```

## Contact

For help and feedback, please feel free to contact [the author](https://github.com/UlugbekSalaev).