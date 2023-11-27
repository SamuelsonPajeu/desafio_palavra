
# Word Relation (API)
A REST API that retrieve related words by scraping Brazilian web dictionaries

![Tests](https://github.com/SamuelsonPajeu/desafio_palavra/actions/workflows/tests.yml/badge.svg)
![Image](https://render-badge-samuelsonpajeu.onrender.com/by_name?projectName=desafio-palavra)

## Install
- Make sure you got:
  * [Python => 3.8](https://www.python.org/downloads/release/python-3818/)
  * [PIP](https://pip.pypa.io/en/stable/installation/)

- Prepare your ENVIROMENT:
  * On this project root directory:

  
   ```bash
   cp .env_template .env
   ```

- Install dependencies
 ```bash
 pip install -r requirements.txt
 ```

- [x] You're ready to run and execute this project:
```bash
 .\manage.py runserver
```

## Usage
- LIVE APPLICATION: https://desafio-palavra.onrender.com
- ENDPOINT: http://127.0.0.1:8000/

#### Get words data

<details>
  <summary><code>GET</code> <code><b>/get_data/{string}</b></code> <code>(Search by word)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `string` |  required | string | Exactly match of a brasilian word |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | JSON       |


##### Example cURL

> ```javascript
>  curl -X GET "http://127.0.0.1:8000/get_data/amor" -H "Content-Type: application/json" -H "accept: */*"
> ```

</details>

------------------------------------------------------------------------------------------
## Config
![image](https://github.com/SamuelsonPajeu/desafio_palavra/assets/79151331/1a21c329-c26b-4e0e-8704-f67512fce9a1)

In the *desafio_palavra_app > config.toml* it's possible to configure some thigs like:

- [urls]:
     ```toml
     word_relation_type = {
       link = "url_here/{}", # The brackets are replaced by the current searched word
       class = "HTML Class Here" # Should be a <ul> element
     }
     ```
- [search]:
  ```toml
     max_results = 50 # Max words returned
  ```

- [cache]
  (When the cache is full, it's replace the less searched word by the new one)
  ```toml
      enabled = true # If it's enabled or not
      max_size = 100 # Max words stored by the cache
   ```

  Cache in usage:
  First search with the word "amor":
   ![image](https://github.com/SamuelsonPajeu/desafio_palavra/assets/79151331/6815ea52-6991-4c9a-ba1a-6abdb0baa119)

  With the data on cache:
  
  ![image](https://github.com/SamuelsonPajeu/desafio_palavra/assets/79151331/b0b79df2-393b-49bd-b070-bf92f0fac0b9)





