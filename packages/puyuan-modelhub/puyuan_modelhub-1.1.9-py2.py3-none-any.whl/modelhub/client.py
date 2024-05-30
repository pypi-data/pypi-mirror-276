from modelhub.utils import BaseModel, retrieve_top_k
import json
import os
import numpy as np
from functools import partial
from io import TextIOWrapper
from typing import Any, Dict, Generator, List, Literal, Optional, Union, AsyncGenerator

import httpx
import retrying
from httpx import Response

import modelhub.constants as constants
from modelhub.types import (
    BaseMessage,
    ChatParameters,
    CrossEncoderOutput,
    CrossEncoderParams,
    EmbeddingOutput,
    ModelInfo,
    ModelInfoOutput,
    NTokensOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    Transcription,
)
from modelhub.types.retrieve import RerankOutput, RetrieveOutput
from .errors import (
    APIConnectionError,
    APIRateLimitError,
    AuthenticationError,
    InternalServerError,
)


class ModelhubClient(BaseModel):
    """
    ModelhubClient: A Python client for the Modelhub API
    """

    user_name: str = os.getenv("MODELHUB_USER_NAME", "")
    """user name for authentication"""
    user_password: str = os.getenv("MODELHUB_USER_PASSWORD", "")
    """user password for authentication"""
    host: str = os.getenv("MODELHUB_HOST", "")
    model: str = ""
    max_retries: int = 3
    wait_fixed: int = 1000
    timeout: Optional[Union[httpx.Timeout, float]] = 600
    """host URL of the Modelhub API"""
    """list of supported models"""
    headers: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers["Authorization"] = f"{self.user_name}:{self.user_password}"
        self.host = self.host.rstrip("/")

    @property
    def supported_models(self) -> Dict[str, ModelInfo]:
        return self._get_supported_models()

    def raise_for_status(self, response: Response, status_code: int, text: str):
        if status_code == constants.ERR_AUTH_FAILED:
            raise AuthenticationError()
        if status_code == constants.ERR_ISE:
            raise InternalServerError(text)
        if status_code == constants.ERR_API_CONNECTION_ERROR:
            raise APIConnectionError(text)
        if status_code == constants.ERR_API_RATE_LIMIT:
            raise APIRateLimitError(text)
        response.raise_for_status()

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=lambda e: not isinstance(e, AuthenticationError),
    )
    def _post(
        self,
        url: str,
        method: Literal["get", "post"] = "post",
        **kwargs,
    ) -> Response:
        """Make a GET request"""
        response = getattr(httpx, method)(
            url=url, timeout=self.timeout, headers=self.headers, **kwargs
        )
        self.raise_for_status(response, response.status_code, response.text)
        return response

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=lambda e: not isinstance(e, AuthenticationError),
    )
    async def _apost(self, url: str, **kwargs) -> Response:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                url, headers=self.headers, timeout=self.timeout, **kwargs
            )
            self.raise_for_status(r, r.status_code, r.text)
            return r

    def _get_supported_models(self) -> ModelInfoOutput:
        """Get a list of supported models from the Modelhub API"""
        response = self._post(
            self.host + "/models",
            method="get",
        )
        return ModelInfoOutput(**response.json()).models

    def n_tokens(self, prompt: str, model: str = "", params={}) -> NTokensOutput:
        """
        Get the number of tokens in a prompt
        params:
            prompt: the prompt
            model: the model name
        """
        model = model or self.model
        response = self._post(
            self.host + "/tokens",
            json={
                "prompt": prompt,
                "model": model,
                "params": params,
            },
        )
        return NTokensOutput(**response.json())

    def chat(
        self,
        prompt: str,
        model: str = "",
        history: List[Union[BaseMessage, Dict[str, Any]]] = [],
        return_type: Literal["text", "json", "regex"] = "text",
        return_schema: Union[Dict[str, Any], str, None] = None,
        parameters: ChatParameters = {},
        **kwargs,
    ) -> TextGenerationOutput:
        model = model or self.model
        parameters["history"] = [
            m.dict() if isinstance(m, BaseMessage) else m for m in history
        ]
        parameters["return_type"] = return_type
        parameters["schema"] = return_schema
        response = self._post(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": {**parameters, **kwargs},
            },
        )
        out = TextGenerationOutput(**response.json())
        return out

    def batch_chat(
        self,
        batch_prompts: List[str],
        model: str = "",
        batch_parameters: List[ChatParameters] = [],
    ):
        model = model or self.model
        response = self._post(
            self.host + "/batch_chat",
            json={
                "batch_prompts": batch_prompts,
                "model": model,
                "batch_parameters": batch_parameters,
            },
        )
        outputs = response.json()
        return [TextGenerationOutput(**output) for output in outputs]

    async def abatch_chat(
        self,
        batch_prompts: List[str],
        model: str = "",
        batch_parameters: List[ChatParameters] = [],
    ):
        model = model or self.model
        response = await self._apost(
            self.host + "/batch_chat",
            json={
                "batch_prompts": batch_prompts,
                "model": model,
                "batch_parameters": batch_parameters,
            },
        )
        outputs = response.json()
        return [TextGenerationOutput(**output) for output in outputs]

    async def achat(
        self,
        prompt: str,
        model: str = "",
        history: List[BaseMessage] = [],
        return_type: Literal["text", "json", "regex"] = "text",
        return_schema: Union[Dict[str, Any], str, None] = None,
        parameters: ChatParameters = {},
    ) -> TextGenerationOutput:
        model = model or self.model
        parameters["history"] = [
            m.dict() if isinstance(m, BaseMessage) else m for m in history
        ]
        parameters["return_type"] = return_type
        parameters["schema"] = return_schema
        response = await self._apost(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
        )
        out = TextGenerationOutput(**response.json())
        return out

    @retrying.retry(wait_fixed=wait_fixed, stop_max_attempt_number=max_retries)
    def stream_chat(
        self,
        prompt: str,
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        model = model or self.model
        parameters["history"] = [
            m.dict() if isinstance(m, BaseMessage) else m for m in history
        ]
        with httpx.Client() as client:
            with client.stream(
                "post",
                url=self.host + "/chat",
                headers=self.headers,
                timeout=self.timeout,
                json={
                    "prompt": prompt,
                    "model": model,
                    "parameters": parameters,
                    "stream": True,
                },
            ) as r:
                for line in r.iter_lines():
                    if line.startswith("data:"):
                        out = TextGenerationStreamOutput(**json.loads(line[5:]))
                        self.raise_for_status(r, out.code, out.msg)
                        yield out

    @retrying.retry(wait_fixed=wait_fixed, stop_max_attempt_number=max_retries)
    async def astream_chat(
        self,
        prompt: str,
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
    ) -> AsyncGenerator[TextGenerationStreamOutput, None]:
        model = model or self.model
        parameters["history"] = [
            m.dict() if isinstance(m, BaseMessage) else m for m in history
        ]
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "post",
                url=self.host + "/chat",
                headers=self.headers,
                timeout=self.timeout,
                json={
                    "prompt": prompt,
                    "model": model,
                    "parameters": parameters,
                    "stream": True,
                },
            ) as r:
                async for line in r.aiter_lines():
                    if line.startswith("data:"):
                        out = TextGenerationStreamOutput(**json.loads(line[5:]))
                        self.raise_for_status(r, out.code, out.msg)
                        yield out

    def retrieve(
        self,
        querys: list[str] | str,
        passages: list[str],
        model: str | None = None,
        embedding_params: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        model = model or self.model
        if isinstance(querys, str):
            querys = [querys]
        embedding = partial(
            self.get_embeddings, model=model, parameters=embedding_params
        )
        query_embeddings = np.array(embedding(querys).embeddings)
        passage_embeddings = np.array(embedding(passages).embeddings)
        return RetrieveOutput(
            **retrieve_top_k(
                passages,
                query_embeddings,
                passage_embeddings,
                top_k,
                threshold,
            )
        )

    async def aretrieve(
        self,
        querys: list[str] | str,
        passages: list[str],
        model: str | None = None,
        embedding_params: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        model = model or self.model
        if isinstance(querys, str):
            querys = [querys]
        embedding = partial(
            self.aget_embeddings, model=model, parameters=embedding_params
        )
        query_embeddings = np.array((await embedding(querys)).embeddings)
        passage_embeddings = np.array((await embedding(passages)).embeddings)
        return RetrieveOutput(
            **retrieve_top_k(
                passages,
                query_embeddings,
                passage_embeddings,
                top_k,
                threshold,
            )
        )

    def rerank(
        self,
        query: str,
        docs: list[str],
        model: str | None = None,
        parameters: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        pairs = [[query, doc] for doc in docs]
        scores = np.array(
            self.cross_embedding(pairs, model=model, parameters=parameters).scores
        )
        idxs = np.argsort(scores)[::-1][:top_k]
        idxs = idxs[scores[idxs] > threshold]
        return RerankOutput(
            passages=[docs[i] for i in idxs],
            idxs=idxs.tolist(),
            scores=scores[idxs].tolist(),
        )

    async def arerank(
        self,
        query: str,
        docs: list[str],
        model: str | None = None,
        parameters: Dict[str, Any] = {},
        top_k: int = 5,
        threshold: float = 0.0,
    ):
        pairs = [[query, doc] for doc in docs]
        scores = np.array(
            (
                await self.across_embedding(pairs, model=model, parameters=parameters)
            ).scores
        )
        idxs = np.argsort(scores)[::-1][:top_k]
        idxs = idxs[scores[idxs] > threshold]
        return RerankOutput(
            passages=[docs[i] for i in idxs],
            idxs=idxs.tolist(),
            scores=scores[idxs].tolist(),
        )

    def get_embeddings(
        self, prompt: str, model: str = "", parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        model = model or self.model
        response = self._post(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
        )
        return EmbeddingOutput(**response.json())

    async def aget_embeddings(
        self, prompt: str, model: str = "", parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        model = model or self.model
        response = await self._apost(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
        )
        return EmbeddingOutput(**response.json())

    def cross_embedding(
        self,
        sentences: List[List[str]],
        model: str = "",
        parameters: CrossEncoderParams = {},
    ) -> CrossEncoderOutput:
        model = model or self.model
        res = self._post(
            self.host + "/cross_embedding",
            json={
                "sentences": sentences,
                "model": model,
                "parameters": parameters,
            },
        )
        return CrossEncoderOutput(**res.json())

    async def across_embedding(
        self,
        sentences: List[List[str]],
        model: str = "",
        parameters: CrossEncoderParams = {},
    ) -> CrossEncoderOutput:
        model = model or self.model
        res = await self._apost(
            self.host + "/cross_embedding",
            json={
                "sentences": sentences,
                "model": model,
                "parameters": parameters,
            },
        )
        return CrossEncoderOutput(**res.json())

    def transcribe(
        self,
        file: Union[str, TextIOWrapper],
        model: str = "",
        language: str = "",
        temperature: float = 0.0,
    ) -> Transcription:
        model = model or self.model
        if isinstance(file, str):
            file = open(file, "rb")

        r = self._post(
            url=self.host + "/audio/transcriptions",
            files={"file": file},
            data={
                "model": model,
                "language": language,
                "temperature": temperature,
            },
        )
        self.raise_for_status(r, r.status_code, r.text)
        return Transcription(**r.json())

    async def atranscribe(
        self,
        file: Union[str, TextIOWrapper],
        model: str = "",
        language: str = "",
        temperature: float = 0.0,
    ) -> Transcription:
        model = model or self.model
        if isinstance(file, str):
            file = open(file, "rb")

        r = await self._apost(
            url=self.host + "/audio/transcriptions",
            files={"file": file},
            data={
                "model": model,
                "language": language,
                "temperature": temperature,
            },
        )
        self.raise_for_status(r, r.status_code, r.text)
        return Transcription(**r.json())


class VLMClient(ModelhubClient):
    """Visual Language Model Client"""

    def chat(self, prompt, image_path, model="cogvlm", parameters={}, **kwargs):
        """
        Chat with a model
        params:
            prompt: the prompt to start the chat
            image_path: the path to the image
            model: the model name
            parameters: the parameters for the model
        """
        image_path = self._post(
            self.host + "/upload",
            files={"file": open(image_path, "rb")},
            params={
                "user_name": self.user_name,
                "user_password": self.user_password,
            },
        ).json()["file_path"]
        parameters["image_path"] = image_path
        return super().chat(prompt=prompt, model=model, parameters=parameters, **kwargs)
