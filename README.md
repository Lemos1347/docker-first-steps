# Docker-first-steps

## Objetivo

Esse repositório tem como objetivo de iniciar meus estudos em um tipo de conteinerização, o `Docker`.

## Containers

Containers são uma maneira de isolar processos locais em sua máquina. Ao contrário de máquinas virtuais, containers utilizam da própria kernel da máquina do usuário para rodar processos isoladamente na mesma arquitetura da máquina também. Containers é um processo nativo da kernel do linux, portanto, quando esses são feitos em windowns e macs, uma máquina virtual linux é executada para conteinizar um processo.

## Docker

Em docker iremos separar em três tópicos:

- Dockerfile
- Dockerignore files
- Docker-compose
- Docker Hub

### Dockerfile

Dockerfile pode ser considerado como um documento de configuração do ambiente isolado da sua máquina, ou seja, o documento de configuração do container. Para exemplificar alguns dos possíveis comandos, criei um exemplo do diretório `/src`. Nesse diretório há uma aplicação mínima feita em python com flask e um `Dockerfile`.

1.  Em um Dockerfile primeiro precisamos importar uma "imagem". Essa "imagem" corresponde a qual "base" que precisamos no container, como `node`, `python` ou até mesmo apenas um `ubuntu`. Fazemos isso com a seguinte linha:

```Dockerfile
FROM python:3.11.2
```

2.  Depois disso, definimos qual será o diretório que iremos trabalhar no container, no caso, "qual pasta ele irá criar e trabalhar em cima".

```Dockerfile
WORKDIR /backend
```

3.  Depois disso, utilizamos da palavra-chave `COPY` para copiar um arquivo que está no diretório padrão da máquina para o diretório criado no container (representado nesse caso por um . , o que significa o destino para o arquivo sendo `/backend`). Nesse caso, é o `requirements.txt`, o qual corresponde as dependências de python que precisamos instalar para rodar a aplicação.

```Dockerfile
COPY requirements.txt .
```

4.  Depois de copiar o arquivo que precisamos, rodaremos um comando no terminal desse container. Fazemos isso com a seguinte linha:

```Dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

5. Depois de configurar todo o container, baixando tudo que precisamos, copiamos tudo que temos no diretório em que o `Dockerfile` se encontra para o diretório de trabalho no container. Com a seguinte linha:

```Dockerfile
COPY . .
```

6. Em um container, limitamos tudo que ele possui e todos os seus acessos à kernel principal do sistema. Por nosso exemplo se tratar de uma backend, ele necessita de uma porta para funcionar corretamente. Assim, iremos expor a porta utilizada na aplicação construída.

```Dockerfile
EXPOSE 3001
```

7. E por fim, colocamos o camndo necessário para rodar a aplicação que está contida no container. Nesse caso, colocamos o que precisa para rodar uma aplicação python:

```Dockerfile
CMD [ "python", "app.py" ]
```

Pronto, agora o documento de configuração do conteiner está pronto!  
Para o próximo passo, precisamos "buildar" esse documento. Fazemos isso com a seguinte linha de comando no terminal em que se encontra o `Dockerfile`:

```shell
docker build .
```

Esse comando gerará um hash do seu `Dockerfile`, o qual servirá para identificá-lo em futuros comandos. O ponto no final, representa a localização do `Dockerfile`, como estamos com o terminal no diretório correto, colocamos apenas um ponto. Caso deseja colocar um nome em sua build, apenas acrescentar o argumento `-t`:

```shell
docker build -t nomedousuario/nomedoprojeto .
```

Depois de um build bem sucedido, podemos rodar um container. Para isso, precisamos apenas do nome da build ou do seu hash. Podemos adicionar o argumento `-d` para que o terminal não fique travado com a operação do container:

```shell
docker run -d nomedousuario/nomedoprojeto
```

Porém, com esse comando vamos apenas conseguir rodar o projeto na porta do container. Para conseguirmos enxergar o que cada rota retorna, precisamos de realizar um bind das portas do sistema principal com a porta do container:

```shell
docker run -d -p 80:3001 nomedousuario/nomedoprojeto
```

Nesse comando, os primeiro números antes dos `:` representa as portas do sistema princial e os após representa as portas do container.  
Pronto! O seu primeiro container está funcionando!

### Dockerignore files

Em um projeto temos várias pastas e arquivos que nem sempre precisamos de tudo para rodar uma aplicação (pode ser desde documentação até uma venv ou um node_modules) os quais não precisam de serem copiados para o container. Para isso, podemos criar um arquivo `.dockerignore` contento os diretórios em que não queremos que sejam levados para o container (similar a um `.gitignore`).

### Docker-compose

O Docker possuí uma outra funcionalidade, se chama `docker-compose`. Isso nada mais é que uma maneira fácil de administrar vários containers ao mesmo tempo. Para isso, criamos um arquivo chamado `docker-compose.yml`. A sua configuração básica para essa aplicação flask é composto pelos seguintes campos:

- `version` -> representa qual a versão a ser utilizada para o docker-compose.
- `services` -> depois temos os services, aqui declararemos quais conteiners queremos "buildar"/"subir". Cada serviço terá um nome pode colocar o que desejar.
- `backend` -> é o nome do primeiro serviço que estamos declarando.
- `build` -> a primeiro informação que damos a esse serviço é onde ele pode localizar um `Dockerfile` para buildar o container. Podemos utilizar também a palavra-chave `image` para caso queremos indicar para o compose uma imagem já "buildada" seja local ou na núvem (mais especificamante, no Docker Hub).
- `container_name` -> nome de identificação para o container referente a esse serviço
- `ports` -> aqui realizamos o bind de portas do sistema com as do container. Os números antes dos `:` é a porta do seu sistema, e os depois é referente as portas do container.
- `volumes` -> volumes possuem várias características e funcionalidades. Nesse caso, o identificamos para "linkar" um diretório no sistema principal com um diretório dentro do container. Nesse caso, os caracteres antes dos `:` representam o diretório no sistema principal, enquanto os após os `:` representam o diretório de dentro do container. Caso esteja tudo correto, agora sempre que houver uma mudança no projeto, não será necessário reiniciar o container (já que configuramos o flask para fazer isso e o docker para identificar as mudanças).

### Docker Hub

Docker Hub nada mais é que um armazenamento em núvem de imagens docker. Nele podemos subir imagens que criamos, com o comando:

```shell
 docker push dockerbuild_name
```

E podemos também baixar:

```shell
docker pull dockerbuild_name
```

Imagens docker podem ser interpretadas como o resultado do "build" de um `Dockerfiles`.
