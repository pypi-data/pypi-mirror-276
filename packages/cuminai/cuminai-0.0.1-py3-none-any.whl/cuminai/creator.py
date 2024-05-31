from itertools import islice
import os
import asyncio
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
    _CUMINAI_KB_VERSION_HEADER,
    _CUMINAI_LATEST_VERSION_HEADER,
    _CUMIN_FILE_NAME,
    _LINK_KIND,
    _TEXT_KIND,
    _PUBLIC_VISIBILITY,
    _GLOBAL_TAGGING,
    _LOCAL_TAGGING,
    _CUMINAI_DUMMY_COLLECTION_NAME,
    _DEFAULT_UPSERT_BATCH_SIZE
)

from cuminai.validator import Validator, UsernameValidator, OllamaEmbeddingFetcher
from langchain_community.embeddings import OllamaEmbeddings
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
@click.option('-olmurl', '--ollamaserviceurl', help='service url of running ollama service', default='http://localhost:11434')
def deploy(projectdir, ollamaserviceurl):
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
    
    try:
        if cuminfile.kind == _LINK_KIND:
            docs = doc_loader.get_link_docs()
        elif cuminfile.kind == _TEXT_KIND:
            docs = doc_loader.get_text_docs()
    except:
        click.echo("knowledge source doesn't exist. Please try again.")
        return

    parser = None
    if hasattr(cuminfile, 'chunkstrategy'):
        parser = Chunker(docs=docs, 
                        chunk_size=cuminfile.chunkstrategy.size, 
                        chunk_overlap=cuminfile.chunkstrategy.overlap)
    else:
        parser = Chunker(docs=docs)
    
    doc_splits = parser.get_chunks()

    if len(doc_splits) == 0 or all(len(doc.page_content) < 10 for doc in doc_splits):
        click.echo("not a credible knowledge source. Please try again.")
        return

    if cuminfile.kind == _TEXT_KIND:
        for chunk in doc_splits:
            chunk.metadata['source'] = utils.get_file_name(chunk.metadata['source'])

    tagger = Tagger(chunks=doc_splits, knowledge=cuminfile.knowledge)

    if not hasattr(cuminfile, 'tag'):
        tagger.add_global_tags()
    elif cuminfile.tag.type == _GLOBAL_TAGGING:
        tagger.add_global_tags()
    elif cuminfile.tag.type == _LOCAL_TAGGING:
        tagger.add_local_tags(cuminfile.tag.minoccurances)

    doc_splits = tagger.get_tagged_chunks()

    match = OllamaEmbeddingFetcher.match(cuminfile.embedding)
    ollama_embedding_name = match.groups(1)[0]

    ollama_check_client = http.client.HTTPConnection('localhost', 11434)
    try:
        ollama_check_client.request(http.HTTPMethod.GET, "/")
        if ollama_check_client.getresponse().status != 200:
            click.echo("Ollama service is unresponsive")
            return
    except ConnectionRefusedError:
        click.echo("Ollama Service not running on client machine. Make sure ollama is installed and running before using Cumin AI")
        return
        

    embedding_function = CuminAIEmbeddings(model=ollama_embedding_name, base_url=ollamaserviceurl)

    is_public_header = "false"
    if cuminfile.type == _PUBLIC_VISIBILITY:
        is_public_header = "true"

    is_latest_version = "false"
    if hasattr(cuminfile.version, 'latest'):
        if cuminfile.version.latest:
            is_latest_version = "true"

    metadata = {
        _CUMINAI_API_KEY_HEADER: creds['apikey'],
        _CUMINAI_KB_NAME_HEADER: cuminfile.name,
        _CUMINAI_IS_PUBLIC_HEADER: is_public_header,
        _CUMINAI_KB_VERSION_HEADER: cuminfile.version.tag,
        _CUMINAI_LATEST_VERSION_HEADER: is_latest_version
    }
    
    client = qdrant_client.QdrantClient(
        url=_CUMINAI_CREATOR_HOST, 
        port=443,
        https=True,
        metadata=metadata
    )

    async_client = qdrant_client.AsyncQdrantClient(
        url=_CUMINAI_CREATOR_HOST, 
        port=443,
        https=True,
        metadata=metadata
    )

    if not client.collection_exists(_CUMINAI_DUMMY_COLLECTION_NAME):
        try:
            Qdrant.construct_instance(
                texts = [chunk.page_content for chunk in doc_splits[:1]], 
                collection_name=_CUMINAI_DUMMY_COLLECTION_NAME,
                embedding=OllamaEmbeddings(model=ollama_embedding_name, base_url=ollamaserviceurl),
                url=_CUMINAI_CREATOR_HOST, 
                port=443,
                https=True,
                metadata=metadata
            )
        except qdrant_client.http.exceptions.UnexpectedResponse as e:
            click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
            return

    try:
        store = Qdrant(
            client=client,
            collection_name=_CUMINAI_DUMMY_COLLECTION_NAME,
            embeddings=embedding_function,
            async_client=async_client
        )

        asyncio.run(_aadd_documents(store, doc_splits))
    except qdrant_client.http.exceptions.UnexpectedResponse as e:
        click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
        return
    except ValueError as e:
        click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
        return
    
    click.echo(f"\nDeployment successful... knowledge is available at @{creds['username']}/{cuminfile.name}:{cuminfile.version.tag}")

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
    
async def _aadd_documents(store, doc_splits):
    tasks = []

    docs_iterator = iter(doc_splits)
    while batch := list(islice(docs_iterator, _DEFAULT_UPSERT_BATCH_SIZE)):
        tasks.append(store.aadd_documents(documents=batch))
    
    await asyncio.gather(*tasks)