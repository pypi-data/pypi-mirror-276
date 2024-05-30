import asyncio
import json
import logging
import uuid
from typing import Optional, Union

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from r2r.core import (
    Document,
    DocumentType,
    GenerationConfig,
    PipeLoggingConnectionSingleton,
    generate_id_from_label,
    generate_run_id,
    to_async_generator,
)
from r2r.pipes import R2REvalPipe

from .r2r_abstractions import R2RPipelines, R2RProviders
from .r2r_config import R2RConfig

MB_CONVERSION_FACTOR = 1024 * 1024

from pydantic import BaseModel

logger = logging.getLogger(__name__)


def syncable(func):
    """Decorator to mark methods for synchronous wrapper creation."""
    func._syncable = True
    return func


class AsyncSyncMeta(type):
    _event_loop = None  # Class-level shared event loop

    @classmethod
    def get_event_loop(cls):
        if cls._event_loop is None or cls._event_loop.is_closed():
            cls._event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls._event_loop)
        return cls._event_loop

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        for attr_name, attr_value in dct.items():
            if asyncio.iscoroutinefunction(attr_value) and getattr(
                attr_value, "_syncable", False
            ):
                sync_method_name = attr_name[
                    1:
                ]  # Remove leading 'a' for sync method
                async_method = attr_value

                def make_sync_method(async_method):
                    def sync_wrapper(self, *args, **kwargs):
                        loop = cls.get_event_loop()
                        if not loop.is_running():
                            # Setup to run the loop in a background thread if necessary
                            # to prevent blocking the main thread in a synchronous call environment
                            from threading import Thread

                            result = None
                            exception = None

                            def run():
                                nonlocal result, exception
                                try:
                                    asyncio.set_event_loop(loop)
                                    result = loop.run_until_complete(
                                        async_method(self, *args, **kwargs)
                                    )
                                except Exception as e:
                                    exception = e
                                finally:
                                    loop.run_until_complete(
                                        loop.shutdown_asyncgens()
                                    )
                                    loop.close()

                            thread = Thread(target=run)
                            thread.start()
                            thread.join()
                            if exception:
                                raise exception
                            return result
                        else:
                            # If there's already a running loop, schedule and execute the coroutine
                            future = asyncio.run_coroutine_threadsafe(
                                async_method(self, *args, **kwargs), loop
                            )
                            return future.result()

                    return sync_wrapper

                setattr(
                    new_cls, sync_method_name, make_sync_method(async_method)
                )
        return new_cls


class R2RApp(metaclass=AsyncSyncMeta):
    """Main class for the R2R application.

    This class is responsible for setting up the FastAPI application and
    defining the routes for the various endpoints. It also contains the
    synchronous wrappers for the asynchronous methods defined in the class.

    Endpoints are provided to:
    - Ingest documents
    - Ingest files
    - Search
    - Retrieve and generate completions
    - Delete entries
    - Retrieve user IDs
    - Retrieve user document data
    - Retrieve logs
    """

    def __init__(
        self,
        config: R2RConfig,
        providers: R2RProviders,
        pipelines: R2RPipelines,
        do_apply_cors: bool = True,
        *args,
        **kwargs,
    ):
        self.config = config
        self.providers = providers
        self.logging_connection = PipeLoggingConnectionSingleton()
        self.ingestion_pipeline = pipelines.ingestion_pipeline
        self.search_pipeline = pipelines.search_pipeline
        self.rag_pipeline = pipelines.rag_pipeline
        self.streaming_rag_pipeline = pipelines.streaming_rag_pipeline
        self.eval_pipeline = pipelines.eval_pipeline

        self.app = FastAPI()

        if do_apply_cors:
            R2RApp._apply_cors(self.app)

        self._setup_routes()

    def _setup_routes(self):
        self.app.add_api_route(
            path="/ingest_documents/",
            endpoint=self.ingest_documents_app,
            methods=["POST"],
        )
        self.app.add_api_route(
            path="/ingest_files/",
            endpoint=self.ingest_files_app,
            methods=["POST"],
        )
        self.app.add_api_route(
            path="/search/", endpoint=self.search_app, methods=["POST"]
        )
        self.app.add_api_route(
            path="/rag/", endpoint=self.rag_app, methods=["POST"]
        )
        self.app.add_api_route(
            path="/evaluate/",
            endpoint=self.evaluate_app,
            methods=["POST"],
        )
        self.app.add_api_route(
            path="/delete/", endpoint=self.delete_app, methods=["DELETE"]
        )
        self.app.add_api_route(
            path="/get_user_ids/",
            endpoint=self.get_user_ids_app,
            methods=["GET"],
        )
        self.app.add_api_route(
            path="/get_user_document_data/",
            endpoint=self.get_user_document_data_app,
            methods=["POST"],
        )
        self.app.add_api_route(
            path="/get_logs/",
            endpoint=self.get_logs_app,
            methods=["POST"],
        )

        self.app.add_api_route(
            path="/get_open_api_endpoint/",
            endpoint=self.get_open_api_endpoint,
            methods=["POST"],
        )
        # self.app.include_router(self.app.router)

    @syncable
    async def aingest_documents(self, documents: list[Document]):
        try:
            # Process the documents through the pipeline
            await self.ingestion_pipeline.run(
                input=to_async_generator(documents)
            )
            return {"results": "Entries upserted successfully."}
        except Exception as e:
            logger.error(
                f"ingest_documents(documents={documents}) - \n\n{str(e)})"
            )
            raise HTTPException(status_code=500, detail=str(e))

    class IngestDocumentsRequest(BaseModel):
        documents: list[Document]

    async def ingest_documents_app(self, request: IngestDocumentsRequest):
        try:
            return await self.aingest_documents(request.documents)
        except Exception as e:
            run_id = self.ingestion_pipeline.run_id or generate_run_id()
            await self.ingestion_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="pipeline_type",
                value=self.ingestion_pipeline.pipeline_type,
                is_pipeline_info=True,
            )

            await self.ingestion_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="error",
                value=str(e),
                is_pipeline_info=False,
            )
            raise HTTPException(status_code=500, detail=str(e))

    @syncable
    async def aingest_files(
        self,
        files: list[UploadFile],
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[uuid.UUID]] = None,
    ):
        if metadatas and len(metadatas) != len(files):
            raise HTTPException(
                status_code=400,
                detail="Number of metadata entries does not match number of files.",
            )
        if ids and len(ids) != len(files):
            raise HTTPException(
                status_code=400,
                detail="Number of ids does not match number of files.",
            )
        if len(files) == 0:
            raise HTTPException(
                status_code=400, detail="No files provided for ingestion."
            )

        try:
            documents = []
            for iteration, file in enumerate(files):
                logger.info(f"Processing file: {file.filename}")
                if (
                    file.size
                    > self.config.app.get("max_file_size_in_mb", 32)
                    * MB_CONVERSION_FACTOR
                ):
                    logger.error(f"File size exceeds limit: {file.filename}")
                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds maximum allowed size.",
                    )
                if not file.filename:
                    logger.error("File name not provided.")
                    raise HTTPException(
                        status_code=400, detail="File name not provided."
                    )

                file_content = await file.read()
                logger.info(f"File read successfully: {file.filename}")

                document_id = (
                    generate_id_from_label(file.filename)
                    if ids is None
                    else ids[iteration]
                )
                document_metadata = metadatas[iteration] if metadatas else {}

                documents.append(
                    Document(
                        id=document_id,
                        type=DocumentType(file.filename.split(".")[-1]),
                        data=file_content,
                        metadata=document_metadata,
                    )
                )
                logger.info(f"Document created: {document_id}")

            # Run the pipeline asynchronously
            logger.info("Running the ingestion pipeline...")
            await self.ingestion_pipeline.run(
                input=to_async_generator(documents),
            )
            logger.info("Ingestion pipeline completed.")

            return {
                "results": [
                    f"File '{file.filename}' processed successfully."
                    for file in files
                ]
            }
        except Exception as e:
            logger.error(
                f"ingest_files(metadata={metadatas}, ids={ids}, files={files}) - \n\n{str(e)})"
            )
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Ensure all file handles are closed
            for file in files:
                file.file.close()

    async def ingest_files_app(
        self,
        files: list[UploadFile] = File(...),
        metadatas: Optional[str] = Form(None),
        ids: Optional[str] = Form(None),
    ):
        """Ingest files into the system."""
        try:
            if ids and ids != "null":
                ids_list = json.loads(ids)
                if len(ids_list) != 0:
                    try:
                        ids_list = [uuid.UUID(id) for id in ids_list]
                    except ValueError:
                        raise HTTPException(
                            status_code=400, detail="Invalid UUID provided."
                        )
            else:
                ids_list = None

            # Parse metadatas if provided
            metadatas = (
                json.loads(metadatas)
                if metadatas and metadatas != "null"
                else None
            )

            # Call aingest_files with the correct order of arguments
            return await self.aingest_files(
                files=files, metadatas=metadatas, ids=ids_list
            )
        except Exception as e:
            logger.error(f"ingest_files() - \n\n{str(e)})")
            run_id = self.ingestion_pipeline.run_id or generate_run_id()
            await self.ingestion_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="pipeline_type",
                value=self.ingestion_pipeline.pipeline_type,
                is_pipeline_info=True,
            )

            await self.ingestion_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="error",
                value=str(e),
                is_pipeline_info=False,
            )
            raise HTTPException(status_code=500, detail=str(e))

    @syncable
    async def asearch(
        self,
        query: str,
        search_filters: Optional[dict] = None,
        search_limit: int = 10,
    ):
        """Search for documents based on the query."""
        try:
            search_filters = search_filters or {}
            results = await self.search_pipeline.run(
                input=to_async_generator([query]),
                search_filters=search_filters,
                search_limit=search_limit,
            )
            return {"results": [results.dict() for results in results]}
        except Exception as e:
            logger.error(f"search(query={query}) - \n\n{str(e)})")
            raise HTTPException(status_code=500, detail=str(e))

    class SearchRequest(BaseModel):
        query: str
        search_filters: Optional[str] = None
        search_limit: int = 10

    async def search_app(self, request: SearchRequest):
        try:
            search_filters = (
                {}
                if request.search_filters is None
                or request.search_filters == "null"
                else json.loads(request.search_filters)
            )
            return await self.asearch(
                request.query, search_filters, request.search_limit
            )
        except Exception as e:
            # TODO - Make this more modular
            run_id = self.search_pipeline.run_id or generate_run_id()
            await self.search_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="pipeline_type",
                value=self.search_pipeline.pipeline_type,
                is_pipeline_info=True,
            )

            await self.search_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="error",
                value=str(e),
                is_pipeline_info=False,
            )
            raise HTTPException(status_code=500, detail=str(e))

    @syncable
    async def arag(
        self,
        message: str,
        rag_generation_config: GenerationConfig,
        search_filters: Optional[dict[str, str]] = None,
        search_limit: int = 10,
    ):
        try:
            if rag_generation_config.stream:

                async def stream_response():
                    async for chunk in await self.streaming_rag_pipeline.run(
                        input=to_async_generator([message]),
                        streaming=True,
                        search_filters=search_filters,
                        search_limit=search_limit,
                        rag_generation_config=rag_generation_config,
                    ):
                        yield chunk

                return stream_response()

            else:
                results = await self.rag_pipeline.run(
                    input=to_async_generator([message]),
                    streaming=False,
                    search_filters=search_filters,
                    search_limit=search_limit,
                    rag_generation_config=rag_generation_config,
                )
                return results
        except Exception as e:
            logger.error(f"rag(message={message}) - \n\n{str(e)})")
            raise HTTPException(status_code=500, detail=str(e))

    class RAGRequest(BaseModel):
        message: str
        search_filters: Optional[str] = None
        search_limit: int = 10
        rag_generation_config: Optional[str] = None
        streaming: Optional[bool] = None

    async def rag_app(self, request: RAGRequest):
        try:
            search_filters = (
                None
                if request.search_filters is None
                or request.search_filters == "null"
                else json.loads(request.search_filters)
            )
            rag_generation_config = (
                GenerationConfig(
                    **json.loads(request.rag_generation_config),
                    stream=request.streaming,
                )
                if request.rag_generation_config
                and request.rag_generation_config != "null"
                else GenerationConfig(
                    model="gpt-3.5-turbo", stream=request.streaming
                )
            )
            response = await self.arag(
                request.message,
                rag_generation_config,
                search_filters,
                request.search_limit,
            )
            if request.streaming:
                return StreamingResponse(
                    response, media_type="application/json"
                )
            else:
                return {"results": response}

        except Exception as e:
            # TODO - Make this more modular
            run_id = self.rag_pipeline.run_id or generate_run_id()
            await self.rag_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="pipeline_type",
                value=self.rag_pipeline.pipeline_type,
                is_pipeline_info=True,
            )

            await self.rag_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="error",
                value=str(e),
                is_pipeline_info=False,
            )
            raise HTTPException(status_code=500, detail=str(e))

    @syncable
    async def aevaluate(
        self,
        query: str,
        context: str,
        completion: str,
    ):
        try:
            eval_payload = R2REvalPipe.EvalPayload(
                query=query,
                context=context,
                completion=completion,
            )
            result = await self.eval_pipeline.run(
                input=to_async_generator([eval_payload])
            )
            return {"results": result}
        except Exception as e:
            logger.error(f"evaluate(query={query}) - \n\n{str(e)})")
            raise HTTPException(status_code=500, detail=str(e))

    class EvalRequest(BaseModel):
        query: str
        context: str
        completion: str

    async def evaluate_app(self, request: EvalRequest):
        try:
            return await self.aevaluate(
                query=request.query,
                context=request.context,
                completion=request.completion,
            )
        except Exception as e:
            run_id = self.eval_pipeline.run_id or generate_run_id()
            await self.eval_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="pipeline_type",
                value=self.eval_pipeline.pipeline_type,
                is_pipeline_info=True,
            )

            await self.eval_pipeline.pipe_logger.log(
                pipe_run_id=run_id,
                key="error",
                value=str(e),
                is_pipeline_info=False,
            )
            raise HTTPException(status_code=500, detail=str(e))

    @syncable
    async def adelete(self, key: str, value: Union[bool, int, str]):
        try:
            self.providers.vector_db.delete_by_metadata(key, value)
            return {"results": "Entries deleted successfully."}
        except Exception as e:
            logger.error(
                f":delete: [Error](key={key}, value={value}, error={str(e)})"
            )
            raise HTTPException(status_code=500, detail=str(e))

    class DeleteRequest(BaseModel):
        key: str
        value: Union[bool, int, str]

    async def delete_app(self, request: DeleteRequest = Body(...)):
        return await self.adelete(request.key, request.value)

    @syncable
    async def aget_user_ids(self):
        try:
            user_ids = self.providers.vector_db.get_metadatas(
                metadata_fields=["user_id"]
            )

            return {"results": [ele["user_id"] for ele in user_ids]}
        except Exception as e:
            logger.error(f"get_user_ids() - \n\n{str(e)})")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_ids_app(self):
        return await self.aget_user_ids()

    @syncable
    async def aget_user_document_data(self, user_id: str):
        try:
            if isinstance(user_id, uuid.UUID):
                user_id = str(user_id)
            document_ids = self.providers.vector_db.get_metadatas(
                metadata_fields=["document_id", "title"],
                filter_field="user_id",
                filter_value=user_id,
            )
            return {"results": [ele for ele in document_ids]}
        except Exception as e:
            logger.error(
                f"get_user_document_data(user_id={user_id}) - \n\n{str(e)})"
            )
            raise HTTPException(status_code=500, detail=str(e))

    class UserDocumentRequest(BaseModel):
        user_id: str

    async def get_user_document_data_app(self, request: UserDocumentRequest):
        return await self.aget_user_document_data(request.user_id)

    @syncable
    async def aget_logs(self, pipeline_type: Optional[str] = None):
        try:
            logs_per_run = 10
            if self.logging_connection is None:
                raise HTTPException(
                    status_code=404, detail="Logging provider not found."
                )
            run_info = await self.logging_connection.get_run_info(
                pipeline_type=pipeline_type,
                limit=self.config.app.get("max_logs", 100) // logs_per_run,
            )
            run_ids = [run.run_id for run in run_info]
            if len(run_ids) == 0:
                return {"results": []}
            logs = await self.logging_connection.get_logs(run_ids)
            # Aggregate logs by run_id and include run_type
            aggregated_logs = []

            for run in run_info:
                run_logs = [
                    log for log in logs if log["pipe_run_id"] == run.run_id
                ]
                entries = [
                    {"key": log["key"], "value": log["value"]}
                    for log in run_logs
                ]
                aggregated_logs.append(
                    {
                        "run_id": run.run_id,
                        "run_type": run.pipeline_type,
                        "entries": entries,
                    }
                )

            return {"results": aggregated_logs}

        except Exception as e:
            logger.error(f":logs: [Error](error={str(e)})")
            raise HTTPException(status_code=500, detail=str(e))

    class LogsRequest(BaseModel):
        pipeline_type: Optional[str] = None

    async def get_logs_app(self, request: LogsRequest):
        return await self.aget_logs(request.pipeline_type)

    def get_open_api_endpoint(self):
        from fastapi.openapi.utils import get_openapi

        return {
            "results": get_openapi(
                title="R2R Application API",
                version="1.0.0",
                routes=self.app.routes,
            )
        }

    def serve(self, host: str = "0.0.0.0", port: int = 8000):
        try:
            import uvicorn
        except ImportError:
            raise ImportError(
                "Please install uvicorn using 'pip install uvicorn'"
            )

        uvicorn.run(self.app, host=host, port=port)

    @staticmethod
    def _apply_cors(app):
        # CORS setup
        origins = [
            "*",  # TODO - Change this to the actual frontend URL
            "http://localhost:3000",
            "http://localhost:8000",
        ]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,  # Allows specified origins
            allow_credentials=True,
            allow_methods=["*"],  # Allows all methods
            allow_headers=["*"],  # Allows all headers
        )
