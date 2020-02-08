# ksp-compare-backend

### Complete app structure

![diagram with data flow](./ksp-tool.png)

**nginx** serves static files and redirects /api/* calls to **chemy**.  
**chemy** queries **mongo** to retrieve compounds based on input ions.  
**nginx** container communicates with **chemy** over the unix socket on shared
volume.  
**nginx** exposed on port 80 to the outside world.

### Build and deployment

1. Clone or update submodule  
`git submodule update --init --remote`
2. Build docker images  
`docker-compose build`
3. Deploy app  
`docker-compose up -d`


### Chemy

Chemy - Flask app which takes list of ions and returns:  

- if one ion specified - list of compounds with this ion
- if many ios specified - list of compounds which consisted of all possible 
ion combinations

URL: /compounds/  
Method: POST  
Input has to be valid JSON list.  
Input example: `["[Fe(CN^1-)6]^4-"]`  
Response format:

```json
[
  {
    "_id": {
      "$oid": "5e3e91abf543bd00069b1cbc"
    },
    "name": "Ag4[Fe(CN)6]",
    "ions": [
      "Ag^1+",
      "[Fe(CN^1-)6]^4-"
    ],
    "cations": [
      "Ag^1+"
    ],
    "anions": [
      "[Fe(CN^1-)6]^4-"
    ],
    "dissotiation": "<=> 4 Ag^1+  +  [Fe(CN^1-)6]^4-",
    "ksp": "8.5e-45",
    "comment": "",
    "colors": [
      {
        "name": "Orange-red",
        "code": "#FF4400"
      }
    ]
  }
]
```
Run chemy unittests  

```shell script
PYTHONPATH=. python -m unittest -v
```

### Data import from CSV into MongoDB

The **csv\_to\_mongo.py** script loads the whole CSV into memory - it's not 
intended to work with big files.  

Script is started by chemy container before Chemy startup. It cleans MongoDB 
collection and inserts data loaded from CSV.  

#### Parsing

```
<compound>,"<cation1>,<cation2>","<anion1>,<anion2>",<dissociation>,<ksp>,<logpr>,<comment>,"<color_name1>,<color_name2>","<color_code1>,<color_code2>",link
```  
into  

```json
{
  "name": "<compound>",
  "ions": [
    "<cation1>",
    "cation2",
    "anion1",
    "anion2"
  ],
  "cations": [
    "<cation1>",
    "cation2"
  ],
  "anions": [
    "anion1",
    "anion2"
  ],
  "dissociation": "<dissociation>",
  "ksp": "<ksp>",
  "comment": "<comment>",
  "colors": [
    {
      "name": "<name1>",
      "code": "<code1>"
    },
    {
      "name": "<name2>",
      "code": "<code2>"
    }
  ]
}
```
