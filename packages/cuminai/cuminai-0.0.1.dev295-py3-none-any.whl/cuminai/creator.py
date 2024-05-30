import os
import click
from pathlib import Path
import http.client
import yaml
from cuminai.constants import (
    _CUMINAI_CONFIG_DIR,
    _CUMINAI_CONFIG_FILE,
    _CUMINAI_CREATOR_HOST,
    _CUMINAI_CREATOR_HOST_NAME,
    _CUMINAI_API_KEY_HEADER,
    _CUMINAI_CLIENT_ID_HEADER,
    _CUMINAI_KB_NAME_HEADER,
    _CUMINAI_IS_PUBLIC_HEADER,
    _CUMIN_FILE_NAME,
    _LINK_KIND,
    _TEXT_KIND,
    _PUBLIC_VISIBILITY,
    _GLOBAL_TAGGING,
    _LOCAL_TAGGING,
    _CUMINAI_DUMMY_COLLECTION_NAME,
)

from cuminai.validator import Validator, UsernameValidator, OllamaEmbeddingFetcher

#from langchain_community.embeddings import OllamaEmbeddings
import qdrant_client
from langchain_qdrant import Qdrant
from cuminai.config import Cuminfile
import cuminai.utils as utils
from cuminai.chunker import Chunker
from cuminai.document_loader import Loader
from cuminai.tagger import Tagger
from cuminai.embedding import CuminAIEmbeddings
import logging
logging.getLogger().setLevel(logging.ERROR)

@click.group()
def executor():
    pass

@executor.command(help='Log in to a Cumin AI managed knowledge store')
@click.option('-u', '--username',  help='username', required=True)
@click.option('-k', '--apikey', help='api key', required=True)
def login(username, apikey):
    username = username.strip()
    apikey = apikey.strip()
    
    if not UsernameValidator.match(username):
        click.echo("username must be an alphanumeric between 6 and 36 characters")
        return

    if apikey == "":
        click.echo("apikey can't be empty")
        return

    # validate the client credentials from Cumin AI
    connection = http.client.HTTPSConnection(_CUMINAI_CREATOR_HOST_NAME, timeout=10)
    connection.request("GET", "/v1/login/verify", headers={
        _CUMINAI_API_KEY_HEADER: apikey,
        _CUMINAI_CLIENT_ID_HEADER: username
    })
    response = connection.getresponse()
    if response.status != 200:
        click.echo("Login failed: invalid client credentials. please try again with correct username and apikey combination.")
        return

    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        os.makedirs(Path.home() / _CUMINAI_CONFIG_DIR)
        with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'x') as f:
            yaml.dump(None, f)

    data = {}
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        if data is None:
            data = {}

    data["username"] = username
    data["apikey"] = apikey
        
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'w') as f:
        yaml.dump(data, f)

    click.echo(f'Cumin AI login Successful for creator:{username}')

@executor.command(help='Log out from Cumin AI managed knowledge store')
def logout():
    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        click.echo(f'Creator not logged in yet. "cuminai login" first before logging out')
        return

    data = {}
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        if data is None:
            data = {}

    if 'username' not in data or 'apikey' not in data:
        click.echo(f'Creator not logged in yet. "cuminai login" first before logging out')
        return
    
    data.pop("username", None)
    data.pop("apikey", None)

    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'w') as f:
        yaml.dump(data, f)
    click.echo(f'Creator logged out successfully from Cumin AI')

@executor.command(help='Validate the CuminFile for any errors')
@click.option('-pdir', '--projectdir', help='path of directory containing CuminFile', default='.')
def validate(projectdir):
    try:
        _validate(projectdir)
        click.echo("cuminfile validation successful. deploy knowledge using 'cuminai deploy'")
    except ValueError as e:
        click.echo(f'cuminfile validation failed {str(e)}')
    except OSError as e:
        click.echo('CUMINFILE.yaml not found. nothing to validate. exiting...')

@executor.command(help='Deploy knowledge to Cumin AI')
@click.option('-pdir', '--projectdir', help='path of directory containing CuminFile', default='.')
def deploy(projectdir):
    click.echo("Validating CUMINFILE...")
    cuminfile = {}
    try:
        cuminfile = _validate(projectdir, get_parsed=True)
        click.echo("validation successful")
    except ValueError as e:
        click.echo(f'cuminfile validation failed {str(e)}')
        return
    except OSError as e:
        click.echo('CUMINFILE.yaml not found. nothing to validate. exiting...')
        return

    click.echo("Fetching creator credentials...")
    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        click.echo("creator not logged in. Run command: 'cuminai login' with username and apikey")
        return
    
    creds = {}

    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        click.echo(f"creator not logged in. Run command: 'cuminai login' with username and apikey")
        return
    
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        if data is None or 'username' not in data or 'apikey' not in data:
            click.echo("creator not logged in. Run command: 'cuminai login' with username and apikey")
            return
        creds['username'] = data['username']
        creds['apikey'] = data['apikey']
    
    click.echo("creator logged in. got credentials")

    doc_loader = Loader(knowledge=cuminfile.knowledge)
    
    if cuminfile.kind == _LINK_KIND:
        docs = doc_loader.get_link_docs()
    elif cuminfile.kind == _TEXT_KIND:
        docs = doc_loader.get_text_docs()

    parser = None
    if hasattr(cuminfile, 'chunkstrategy'):
        parser = Chunker(docs=docs, 
                        chunk_size=cuminfile.chunkstrategy.size, 
                        chunk_overlap=cuminfile.chunkstrategy.overlap)
    else:
        parser = Chunker(docs=docs)
    
    doc_splits = parser.get_chunks()

    if cuminfile.kind == _TEXT_KIND:
        for chunk in doc_splits:
            chunk.metadata['source'] = utils.get_file_name(chunk.metadata['source'])

    tagger = Tagger(chunks=doc_splits, knowledge=cuminfile.knowledge)

    if cuminfile.tag.type == _GLOBAL_TAGGING:
        tagger.add_global_tags()
    elif cuminfile.tag.type == _LOCAL_TAGGING:
        tagger.add_local_tags(cuminfile.tag.minoccurances)

    doc_splits = tagger.get_tagged_chunks()

    match = OllamaEmbeddingFetcher.match(cuminfile.embedding)
    ollama_embedding_name = match.groups(1)[0]
    embedding_function = CuminAIEmbeddings(model=ollama_embedding_name)

    is_public_header = "false"
    if cuminfile.type == _PUBLIC_VISIBILITY:
        is_public_header = "true"

    client = qdrant_client.QdrantClient(
        url=_CUMINAI_CREATOR_HOST, 
        port=443,
        https=True,
        metadata={
            _CUMINAI_API_KEY_HEADER: creds['apikey'],
            _CUMINAI_KB_NAME_HEADER: cuminfile.name,
            _CUMINAI_IS_PUBLIC_HEADER: is_public_header,
        }
    )

    try:
        store = Qdrant(
            client=client,
            collection_name=_CUMINAI_DUMMY_COLLECTION_NAME,
            embeddings=embedding_function,
        )

        store.add_documents(documents=doc_splits)
        click.echo(f"Deployment successful... knowledge is available at @{creds['username']}/{cuminfile.name}")
        return
    except qdrant_client.http.exceptions.UnexpectedResponse as e:
        if e.status_code != 404:
            click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
            return
        click.echo(f"knowledge source {cuminfile.name} doesn't exist.")
    except ValueError as e:
        click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
        return
    
    try:
        click.echo(f"creating knowledge source {cuminfile.name} and uploading knowledge...")
        _ = Qdrant.from_documents(
            documents=doc_splits,
            collection_name=_CUMINAI_DUMMY_COLLECTION_NAME,
            embedding=embedding_function,
            url=_CUMINAI_CREATOR_HOST,
            port=443,
            https=True,
            metadata={
                _CUMINAI_API_KEY_HEADER: creds['apikey'],
                _CUMINAI_KB_NAME_HEADER: cuminfile.name,
                _CUMINAI_IS_PUBLIC_HEADER: is_public_header,
            }
        )
        click.echo(f"Deployment successful... knowledge is available at @{creds['username']}/{cuminfile.name}")
    except qdrant_client.http.exceptions.UnexpectedResponse as e:
        click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
        return
    except ValueError as e:
        click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
        return

def _validate(projectdir, get_parsed=False):
    cuminfile = None
    with open(os.path.join(projectdir, _CUMIN_FILE_NAME), 'r') as f:
        try:
            data = yaml.safe_load(f)
            cuminfile = Cuminfile(**data)
        except:
            raise ValueError("failed to validate CUMINFILE")
    
    validator = Validator(cuminfile=cuminfile)
    validator.validate()

    if get_parsed:
        return validator.get_cuminfile()