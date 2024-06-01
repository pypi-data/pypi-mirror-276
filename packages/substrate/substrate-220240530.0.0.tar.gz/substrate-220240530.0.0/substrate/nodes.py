"""
𐃏 Substrate
@GENERATED FILE
"""
from __future__ import annotations
from .substrate import SubstrateResponse
from .core.corenode import CoreNode
from .core.models import (
    ExperimentalOut,
    RunPythonOut,
    GenerateTextOut,
    MultiGenerateTextOut,
    BatchGenerateTextOut,
    BatchGenerateJSONOut,
    GenerateJSONOut,
    MultiGenerateJSONOut,
    GenerateTextVisionOut,
    Mistral7BInstructOut,
    Mixtral8x7BInstructOut,
    Llama3Instruct8BOut,
    Llama3Instruct70BOut,
    Firellava13BOut,
    GenerateImageOut,
    MultiGenerateImageOut,
    GenerativeEditImageOut,
    MultiGenerativeEditImageOut,
    StableDiffusionXLOut,
    StableDiffusionXLLightningOut,
    StableDiffusionXLInpaintOut,
    StableDiffusionXLControlNetOut,
    StableDiffusionXLIPAdapterOut,
    TranscribeMediaOut,
    GenerateSpeechOut,
    XTTSV2Out,
    RemoveBackgroundOut,
    FillMaskOut,
    UpscaleImageOut,
    SegmentUnderPointOut,
    SegmentAnythingOut,
    EmbedTextOut,
    MultiEmbedTextOut,
    EmbedImageOut,
    MultiEmbedImageOut,
    JinaV2Out,
    CLIPOut,
    CreateVectorStoreOut,
    ListVectorStoresOut,
    DeleteVectorStoreOut,
    QueryVectorStoreOut,
    FetchVectorsOut,
    UpdateVectorsOut,
    DeleteVectorsOut,
)
from .future_dataclass_models import (
    FutureExperimentalOut,
    FutureRunPythonOut,
    FutureGenerateTextOut,
    FutureMultiGenerateTextOut,
    FutureBatchGenerateTextOut,
    FutureBatchGenerateJSONOut,
    FutureGenerateJSONOut,
    FutureMultiGenerateJSONOut,
    FutureGenerateTextVisionOut,
    FutureMistral7BInstructOut,
    FutureMixtral8x7BInstructOut,
    FutureLlama3Instruct8BOut,
    FutureLlama3Instruct70BOut,
    FutureFirellava13BOut,
    FutureGenerateImageOut,
    FutureMultiGenerateImageOut,
    FutureGenerativeEditImageOut,
    FutureMultiGenerativeEditImageOut,
    FutureStableDiffusionXLOut,
    FutureStableDiffusionXLLightningOut,
    FutureStableDiffusionXLInpaintOut,
    FutureStableDiffusionXLControlNetOut,
    FutureStableDiffusionXLIPAdapterOut,
    FutureTranscribeMediaOut,
    FutureGenerateSpeechOut,
    FutureXTTSV2Out,
    FutureRemoveBackgroundOut,
    FutureFillMaskOut,
    FutureUpscaleImageOut,
    FutureSegmentUnderPointOut,
    FutureSegmentAnythingOut,
    FutureEmbedTextOut,
    FutureMultiEmbedTextOut,
    FutureEmbedImageOut,
    FutureMultiEmbedImageOut,
    FutureJinaV2Out,
    FutureCLIPOut,
    FutureCreateVectorStoreOut,
    FutureListVectorStoresOut,
    FutureDeleteVectorStoreOut,
    FutureQueryVectorStoreOut,
    FutureFetchVectorsOut,
    FutureUpdateVectorsOut,
    FutureDeleteVectorsOut,
)


from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from typing_extensions import Literal


class Experimental(CoreNode[ExperimentalOut]):
    """https://substrate.run/nodes#Experimental"""

    def __init__(self, name: str, args: Dict[str, Any], timeout: int = 60, hide: bool = False):
        """
        Args:
            name: Identifier.
            args: Arguments.
            timeout: Timeout in seconds.

        https://substrate.run/nodes#Experimental
        """
        super().__init__(name=name, args=args, timeout=timeout, hide=hide, out_type=ExperimentalOut)
        self.node = "Experimental"

    @property
    def future(self) -> FutureExperimentalOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#Experimental
        """
        return super().future  # type: ignore


class RunPython(CoreNode[RunPythonOut]):
    """https://substrate.run/nodes#RunPython"""

    def __init__(
        self,
        code: str,
        input: Optional[Dict[str, Any]] = None,
        pip_install: Optional[List[str]] = None,
        hide: bool = False,
    ):
        """
        Args:
            code: Python code to execute. In your code, access values from the `input` parameter using the `SB_IN` variable. Update the `SB_OUT` variable with results you want returned in `output`.
            input: Input to your code, accessible using the preloaded `SB_IN` variable.
            pip_install: Python packages to install. You must import them in your code.

        https://substrate.run/nodes#RunPython
        """
        super().__init__(
            code=code,
            input=input,
            pip_install=pip_install,
            hide=hide,
            out_type=RunPythonOut,
        )
        self.node = "RunPython"

    @property
    def future(self) -> FutureRunPythonOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#RunPython
        """
        return super().future  # type: ignore


class GenerateText(CoreNode[GenerateTextOut]):
    """https://substrate.run/nodes#GenerateText"""

    def __init__(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        node: Literal[
            "Mistral7BInstruct",
            "Mixtral8x7BInstruct",
            "Llama3Instruct8B",
            "Llama3Instruct70B",
        ] = "Mistral7BInstruct",
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.
            node: Selected node.

        https://substrate.run/nodes#GenerateText
        """
        super().__init__(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            node=node,
            hide=hide,
            out_type=GenerateTextOut,
        )
        self.node = "GenerateText"

    @property
    def future(self) -> FutureGenerateTextOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#GenerateText
        """
        return super().future  # type: ignore


class GenerateJSON(CoreNode[GenerateJSONOut]):
    """https://substrate.run/nodes#GenerateJSON"""

    def __init__(
        self,
        prompt: str,
        json_schema: Dict[str, Any],
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        node: Literal["Mistral7BInstruct", "Mixtral8x7BInstruct", "Llama3Instruct8B"] = "Mistral7BInstruct",
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            json_schema: JSON schema to guide `json_object` response.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.
            node: Selected node.

        https://substrate.run/nodes#GenerateJSON
        """
        super().__init__(
            prompt=prompt,
            json_schema=json_schema,
            temperature=temperature,
            max_tokens=max_tokens,
            node=node,
            hide=hide,
            out_type=GenerateJSONOut,
        )
        self.node = "GenerateJSON"

    @property
    def future(self) -> FutureGenerateJSONOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#GenerateJSON
        """
        return super().future  # type: ignore


class MultiGenerateText(CoreNode[MultiGenerateTextOut]):
    """https://substrate.run/nodes#MultiGenerateText"""

    def __init__(
        self,
        prompt: str,
        num_choices: int,
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        node: Literal[
            "Mistral7BInstruct",
            "Mixtral8x7BInstruct",
            "Llama3Instruct8B",
            "Llama3Instruct70B",
        ] = "Mistral7BInstruct",
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            num_choices: Number of choices to generate.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.
            node: Selected node.

        https://substrate.run/nodes#MultiGenerateText
        """
        super().__init__(
            prompt=prompt,
            num_choices=num_choices,
            temperature=temperature,
            max_tokens=max_tokens,
            node=node,
            hide=hide,
            out_type=MultiGenerateTextOut,
        )
        self.node = "MultiGenerateText"

    @property
    def future(self) -> FutureMultiGenerateTextOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#MultiGenerateText
        """
        return super().future  # type: ignore


class BatchGenerateText(CoreNode[BatchGenerateTextOut]):
    """https://substrate.run/nodes#BatchGenerateText"""

    def __init__(
        self,
        prompts: List[str],
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompts: Batch input prompts.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#BatchGenerateText
        """
        super().__init__(
            prompts=prompts,
            temperature=temperature,
            max_tokens=max_tokens,
            hide=hide,
            out_type=BatchGenerateTextOut,
        )
        self.node = "BatchGenerateText"

    @property
    def future(self) -> FutureBatchGenerateTextOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#BatchGenerateText
        """
        return super().future  # type: ignore


class MultiGenerateJSON(CoreNode[MultiGenerateJSONOut]):
    """https://substrate.run/nodes#MultiGenerateJSON"""

    def __init__(
        self,
        prompt: str,
        json_schema: Dict[str, Any],
        num_choices: int,
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        node: Literal["Mistral7BInstruct", "Mixtral8x7BInstruct", "Llama3Instruct8B"] = "Mistral7BInstruct",
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            json_schema: JSON schema to guide `json_object` response.
            num_choices: Number of choices to generate.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.
            node: Selected node.

        https://substrate.run/nodes#MultiGenerateJSON
        """
        super().__init__(
            prompt=prompt,
            json_schema=json_schema,
            num_choices=num_choices,
            temperature=temperature,
            max_tokens=max_tokens,
            node=node,
            hide=hide,
            out_type=MultiGenerateJSONOut,
        )
        self.node = "MultiGenerateJSON"

    @property
    def future(self) -> FutureMultiGenerateJSONOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#MultiGenerateJSON
        """
        return super().future  # type: ignore


class BatchGenerateJSON(CoreNode[BatchGenerateJSONOut]):
    """https://substrate.run/nodes#BatchGenerateJSON"""

    def __init__(
        self,
        prompts: List[str],
        json_schema: Dict[str, Any],
        node: Literal["Mistral7BInstruct", "Llama3Instruct8B"] = "Mistral7BInstruct",
        temperature: float = 0.4,
        max_tokens: Optional[int] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompts: Batch input prompts.
            json_schema: JSON schema to guide `json_object` response.
            node: Selected node.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#BatchGenerateJSON
        """
        super().__init__(
            prompts=prompts,
            json_schema=json_schema,
            node=node,
            temperature=temperature,
            max_tokens=max_tokens,
            hide=hide,
            out_type=BatchGenerateJSONOut,
        )
        self.node = "BatchGenerateJSON"

    @property
    def future(self) -> FutureBatchGenerateJSONOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#BatchGenerateJSON
        """
        return super().future  # type: ignore


class Mistral7BInstruct(CoreNode[Mistral7BInstructOut]):
    """https://substrate.run/nodes#Mistral7BInstruct"""

    def __init__(
        self,
        prompt: str,
        num_choices: int = 1,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            num_choices: Number of choices to generate.
            json_schema: JSON schema to guide response.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#Mistral7BInstruct
        """
        super().__init__(
            prompt=prompt,
            num_choices=num_choices,
            json_schema=json_schema,
            temperature=temperature,
            max_tokens=max_tokens,
            hide=hide,
            out_type=Mistral7BInstructOut,
        )
        self.node = "Mistral7BInstruct"

    @property
    def future(self) -> FutureMistral7BInstructOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#Mistral7BInstruct
        """
        return super().future  # type: ignore


class Mixtral8x7BInstruct(CoreNode[Mixtral8x7BInstructOut]):
    """https://substrate.run/nodes#Mixtral8x7BInstruct"""

    def __init__(
        self,
        prompt: str,
        num_choices: int = 1,
        json_schema: Optional[Dict[str, Any]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            num_choices: Number of choices to generate.
            json_schema: JSON schema to guide response.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#Mixtral8x7BInstruct
        """
        super().__init__(
            prompt=prompt,
            num_choices=num_choices,
            json_schema=json_schema,
            temperature=temperature,
            max_tokens=max_tokens,
            hide=hide,
            out_type=Mixtral8x7BInstructOut,
        )
        self.node = "Mixtral8x7BInstruct"

    @property
    def future(self) -> FutureMixtral8x7BInstructOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#Mixtral8x7BInstruct
        """
        return super().future  # type: ignore


class Llama3Instruct8B(CoreNode[Llama3Instruct8BOut]):
    """https://substrate.run/nodes#Llama3Instruct8B"""

    def __init__(
        self,
        prompt: str,
        num_choices: int = 1,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_schema: Optional[Dict[str, Any]] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            num_choices: Number of choices to generate.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.
            json_schema: JSON schema to guide response.

        https://substrate.run/nodes#Llama3Instruct8B
        """
        super().__init__(
            prompt=prompt,
            num_choices=num_choices,
            temperature=temperature,
            max_tokens=max_tokens,
            json_schema=json_schema,
            hide=hide,
            out_type=Llama3Instruct8BOut,
        )
        self.node = "Llama3Instruct8B"

    @property
    def future(self) -> FutureLlama3Instruct8BOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#Llama3Instruct8B
        """
        return super().future  # type: ignore


class Llama3Instruct70B(CoreNode[Llama3Instruct70BOut]):
    """https://substrate.run/nodes#Llama3Instruct70B"""

    def __init__(
        self,
        prompt: str,
        num_choices: int = 1,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Input prompt.
            num_choices: Number of choices to generate.
            temperature: Sampling temperature to use. Higher values make the output more random, lower values make the output more deterministic.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#Llama3Instruct70B
        """
        super().__init__(
            prompt=prompt,
            num_choices=num_choices,
            temperature=temperature,
            max_tokens=max_tokens,
            hide=hide,
            out_type=Llama3Instruct70BOut,
        )
        self.node = "Llama3Instruct70B"

    @property
    def future(self) -> FutureLlama3Instruct70BOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#Llama3Instruct70B
        """
        return super().future  # type: ignore


class GenerateTextVision(CoreNode[GenerateTextVisionOut]):
    """https://substrate.run/nodes#GenerateTextVision"""

    def __init__(
        self,
        prompt: str,
        image_uris: List[str],
        max_tokens: int = 800,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Text prompt.
            image_uris: Image prompts.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#GenerateTextVision
        """
        super().__init__(
            prompt=prompt,
            image_uris=image_uris,
            max_tokens=max_tokens,
            hide=hide,
            out_type=GenerateTextVisionOut,
        )
        self.node = "GenerateTextVision"

    @property
    def future(self) -> FutureGenerateTextVisionOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#GenerateTextVision
        """
        return super().future  # type: ignore


class Firellava13B(CoreNode[Firellava13BOut]):
    """https://substrate.run/nodes#Firellava13B"""

    def __init__(
        self,
        prompt: str,
        image_uris: List[str],
        max_tokens: int = 800,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Text prompt.
            image_uris: Image prompts.
            max_tokens: Maximum number of tokens to generate.

        https://substrate.run/nodes#Firellava13B
        """
        super().__init__(
            prompt=prompt,
            image_uris=image_uris,
            max_tokens=max_tokens,
            hide=hide,
            out_type=Firellava13BOut,
        )
        self.node = "Firellava13B"

    @property
    def future(self) -> FutureFirellava13BOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#Firellava13B
        """
        return super().future  # type: ignore


class GenerateImage(CoreNode[GenerateImageOut]):
    """https://substrate.run/nodes#GenerateImage"""

    def __init__(self, prompt: str, store: Optional[str] = None, hide: bool = False):
        """
        Args:
            prompt: Text prompt.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#GenerateImage
        """
        super().__init__(prompt=prompt, store=store, hide=hide, out_type=GenerateImageOut)
        self.node = "GenerateImage"

    @property
    def future(self) -> FutureGenerateImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#GenerateImage
        """
        return super().future  # type: ignore


class MultiGenerateImage(CoreNode[MultiGenerateImageOut]):
    """https://substrate.run/nodes#MultiGenerateImage"""

    def __init__(
        self,
        prompt: str,
        num_images: int,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Text prompt.
            num_images: Number of images to generate.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#MultiGenerateImage
        """
        super().__init__(
            prompt=prompt,
            num_images=num_images,
            store=store,
            hide=hide,
            out_type=MultiGenerateImageOut,
        )
        self.node = "MultiGenerateImage"

    @property
    def future(self) -> FutureMultiGenerateImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#MultiGenerateImage
        """
        return super().future  # type: ignore


class StableDiffusionXL(CoreNode[StableDiffusionXLOut]):
    """https://substrate.run/nodes#StableDiffusionXL"""

    def __init__(
        self,
        prompt: str,
        num_images: int,
        negative_prompt: Optional[str] = None,
        steps: int = 30,
        store: Optional[str] = None,
        height: int = 1024,
        width: int = 1024,
        seeds: Optional[List[int]] = None,
        guidance_scale: float = 7,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Text prompt.
            num_images: Number of images to generate.
            negative_prompt: Negative input prompt.
            steps: Number of diffusion steps.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.
            height: Height of output image, in pixels.
            width: Width of output image, in pixels.
            seeds: Seeds for deterministic generation. Default is a random seed.
            guidance_scale: Higher values adhere to the text prompt more strongly, typically at the expense of image quality.

        https://substrate.run/nodes#StableDiffusionXL
        """
        super().__init__(
            prompt=prompt,
            num_images=num_images,
            negative_prompt=negative_prompt,
            steps=steps,
            store=store,
            height=height,
            width=width,
            seeds=seeds,
            guidance_scale=guidance_scale,
            hide=hide,
            out_type=StableDiffusionXLOut,
        )
        self.node = "StableDiffusionXL"

    @property
    def future(self) -> FutureStableDiffusionXLOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#StableDiffusionXL
        """
        return super().future  # type: ignore


class StableDiffusionXLLightning(CoreNode[StableDiffusionXLLightningOut]):
    """https://substrate.run/nodes#StableDiffusionXLLightning"""

    def __init__(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        num_images: int = 1,
        store: Optional[str] = None,
        height: int = 1024,
        width: int = 1024,
        seeds: Optional[List[int]] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Text prompt.
            negative_prompt: Negative input prompt.
            num_images: Number of images to generate.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.
            height: Height of output image, in pixels.
            width: Width of output image, in pixels.
            seeds: Seeds for deterministic generation. Default is a random seed.

        https://substrate.run/nodes#StableDiffusionXLLightning
        """
        super().__init__(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images=num_images,
            store=store,
            height=height,
            width=width,
            seeds=seeds,
            hide=hide,
            out_type=StableDiffusionXLLightningOut,
        )
        self.node = "StableDiffusionXLLightning"

    @property
    def future(self) -> FutureStableDiffusionXLLightningOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#StableDiffusionXLLightning
        """
        return super().future  # type: ignore


class StableDiffusionXLIPAdapter(CoreNode[StableDiffusionXLIPAdapterOut]):
    """https://substrate.run/nodes#StableDiffusionXLIPAdapter"""

    def __init__(
        self,
        prompt: str,
        image_prompt_uri: str,
        num_images: int,
        ip_adapter_scale: float = 0.5,
        negative_prompt: Optional[str] = None,
        store: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        seeds: Optional[List[int]] = None,
        hide: bool = False,
    ):
        """
        Args:
            prompt: Text prompt.
            image_prompt_uri: Image prompt.
            num_images: Number of images to generate.
            ip_adapter_scale: Controls the influence of the image prompt on the generated output.
            negative_prompt: Negative input prompt.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.
            width: Width of output image, in pixels.
            height: Height of output image, in pixels.
            seeds: Random noise seeds. Default is random seeds for each generation.

        https://substrate.run/nodes#StableDiffusionXLIPAdapter
        """
        super().__init__(
            prompt=prompt,
            image_prompt_uri=image_prompt_uri,
            num_images=num_images,
            ip_adapter_scale=ip_adapter_scale,
            negative_prompt=negative_prompt,
            store=store,
            width=width,
            height=height,
            seeds=seeds,
            hide=hide,
            out_type=StableDiffusionXLIPAdapterOut,
        )
        self.node = "StableDiffusionXLIPAdapter"

    @property
    def future(self) -> FutureStableDiffusionXLIPAdapterOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#StableDiffusionXLIPAdapter
        """
        return super().future  # type: ignore


class StableDiffusionXLControlNet(CoreNode[StableDiffusionXLControlNetOut]):
    """https://substrate.run/nodes#StableDiffusionXLControlNet"""

    def __init__(
        self,
        image_uri: str,
        control_method: Literal["edge", "depth", "illusion"],
        prompt: str,
        num_images: int,
        output_resolution: int = 1024,
        negative_prompt: Optional[str] = None,
        store: Optional[str] = None,
        conditioning_scale: float = 0.5,
        seeds: Optional[List[int]] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Input image.
            control_method: Strategy to control generation using the input image.
            prompt: Text prompt.
            num_images: Number of images to generate.
            output_resolution: Resolution of the output image, in pixels.
            negative_prompt: Negative input prompt.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.
            conditioning_scale: Controls the influence of the input image on the generated output.
            seeds: Random noise seeds. Default is random seeds for each generation.

        https://substrate.run/nodes#StableDiffusionXLControlNet
        """
        super().__init__(
            image_uri=image_uri,
            control_method=control_method,
            prompt=prompt,
            num_images=num_images,
            output_resolution=output_resolution,
            negative_prompt=negative_prompt,
            store=store,
            conditioning_scale=conditioning_scale,
            seeds=seeds,
            hide=hide,
            out_type=StableDiffusionXLControlNetOut,
        )
        self.node = "StableDiffusionXLControlNet"

    @property
    def future(self) -> FutureStableDiffusionXLControlNetOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#StableDiffusionXLControlNet
        """
        return super().future  # type: ignore


class GenerativeEditImage(CoreNode[GenerativeEditImageOut]):
    """https://substrate.run/nodes#GenerativeEditImage"""

    def __init__(
        self,
        image_uri: str,
        prompt: str,
        mask_image_uri: Optional[str] = None,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Original image.
            prompt: Text prompt.
            mask_image_uri: Mask image that controls which pixels are inpainted. If unset, the entire image is edited (image-to-image).
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#GenerativeEditImage
        """
        super().__init__(
            image_uri=image_uri,
            prompt=prompt,
            mask_image_uri=mask_image_uri,
            store=store,
            hide=hide,
            out_type=GenerativeEditImageOut,
        )
        self.node = "GenerativeEditImage"

    @property
    def future(self) -> FutureGenerativeEditImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#GenerativeEditImage
        """
        return super().future  # type: ignore


class MultiGenerativeEditImage(CoreNode[MultiGenerativeEditImageOut]):
    """https://substrate.run/nodes#MultiGenerativeEditImage"""

    def __init__(
        self,
        image_uri: str,
        prompt: str,
        num_images: int,
        mask_image_uri: Optional[str] = None,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Original image.
            prompt: Text prompt.
            num_images: Number of images to generate.
            mask_image_uri: Mask image that controls which pixels are edited (inpainting). If unset, the entire image is edited (image-to-image).
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#MultiGenerativeEditImage
        """
        super().__init__(
            image_uri=image_uri,
            prompt=prompt,
            num_images=num_images,
            mask_image_uri=mask_image_uri,
            store=store,
            hide=hide,
            out_type=MultiGenerativeEditImageOut,
        )
        self.node = "MultiGenerativeEditImage"

    @property
    def future(self) -> FutureMultiGenerativeEditImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#MultiGenerativeEditImage
        """
        return super().future  # type: ignore


class StableDiffusionXLInpaint(CoreNode[StableDiffusionXLInpaintOut]):
    """https://substrate.run/nodes#StableDiffusionXLInpaint"""

    def __init__(
        self,
        image_uri: str,
        prompt: str,
        num_images: int,
        mask_image_uri: Optional[str] = None,
        output_resolution: int = 1024,
        negative_prompt: Optional[str] = None,
        store: Optional[str] = None,
        strength: float = 0.8,
        seeds: Optional[List[int]] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Original image.
            prompt: Text prompt.
            num_images: Number of images to generate.
            mask_image_uri: Mask image that controls which pixels are edited (inpainting). If unset, the entire image is edited (image-to-image).
            output_resolution: Resolution of the output image, in pixels.
            negative_prompt: Negative input prompt.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.
            strength: Controls the strength of the generation process.
            seeds: Random noise seeds. Default is random seeds for each generation.

        https://substrate.run/nodes#StableDiffusionXLInpaint
        """
        super().__init__(
            image_uri=image_uri,
            prompt=prompt,
            num_images=num_images,
            mask_image_uri=mask_image_uri,
            output_resolution=output_resolution,
            negative_prompt=negative_prompt,
            store=store,
            strength=strength,
            seeds=seeds,
            hide=hide,
            out_type=StableDiffusionXLInpaintOut,
        )
        self.node = "StableDiffusionXLInpaint"

    @property
    def future(self) -> FutureStableDiffusionXLInpaintOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#StableDiffusionXLInpaint
        """
        return super().future  # type: ignore


class FillMask(CoreNode[FillMaskOut]):
    """https://substrate.run/nodes#FillMask"""

    def __init__(
        self,
        image_uri: str,
        mask_image_uri: str,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Input image.
            mask_image_uri: Mask image that controls which pixels are inpainted.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#FillMask
        """
        super().__init__(
            image_uri=image_uri,
            mask_image_uri=mask_image_uri,
            store=store,
            hide=hide,
            out_type=FillMaskOut,
        )
        self.node = "FillMask"

    @property
    def future(self) -> FutureFillMaskOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#FillMask
        """
        return super().future  # type: ignore


class RemoveBackground(CoreNode[RemoveBackgroundOut]):
    """https://substrate.run/nodes#RemoveBackground"""

    def __init__(
        self,
        image_uri: str,
        return_mask: bool = False,
        background_color: Optional[str] = None,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Input image.
            return_mask: Return a mask image instead of the original content.
            background_color: Hex value background color. Transparent if unset.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#RemoveBackground
        """
        super().__init__(
            image_uri=image_uri,
            return_mask=return_mask,
            background_color=background_color,
            store=store,
            hide=hide,
            out_type=RemoveBackgroundOut,
        )
        self.node = "RemoveBackground"

    @property
    def future(self) -> FutureRemoveBackgroundOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#RemoveBackground
        """
        return super().future  # type: ignore


class UpscaleImage(CoreNode[UpscaleImageOut]):
    """https://substrate.run/nodes#UpscaleImage"""

    def __init__(self, image_uri: str, store: Optional[str] = None, hide: bool = False):
        """
        Args:
            image_uri: Input image.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#UpscaleImage
        """
        super().__init__(image_uri=image_uri, store=store, hide=hide, out_type=UpscaleImageOut)
        self.node = "UpscaleImage"

    @property
    def future(self) -> FutureUpscaleImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#UpscaleImage
        """
        return super().future  # type: ignore


class SegmentUnderPoint(CoreNode[SegmentUnderPointOut]):
    """https://substrate.run/nodes#SegmentUnderPoint"""

    def __init__(
        self,
        image_uri: str,
        point: Point,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Input image.
            point: Point prompt.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#SegmentUnderPoint
        """
        super().__init__(
            image_uri=image_uri,
            point=point,
            store=store,
            hide=hide,
            out_type=SegmentUnderPointOut,
        )
        self.node = "SegmentUnderPoint"

    @property
    def future(self) -> FutureSegmentUnderPointOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#SegmentUnderPoint
        """
        return super().future  # type: ignore


class SegmentAnything(CoreNode[SegmentAnythingOut]):
    """https://substrate.run/nodes#SegmentAnything"""

    def __init__(
        self,
        image_uri: str,
        point_prompts: Optional[List[Point]] = None,
        box_prompts: Optional[List[BoundingBox]] = None,
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Input image.
            point_prompts: Point prompts, to detect a segment under the point. One of `point_prompts` or `box_prompts` must be set.
            box_prompts: Box prompts, to detect a segment within the bounding box. One of `point_prompts` or `box_prompts` must be set.
            store: Use "hosted" to return an image URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the image data will be returned as a base64-encoded string.

        https://substrate.run/nodes#SegmentAnything
        """
        super().__init__(
            image_uri=image_uri,
            point_prompts=point_prompts,
            box_prompts=box_prompts,
            store=store,
            hide=hide,
            out_type=SegmentAnythingOut,
        )
        self.node = "SegmentAnything"

    @property
    def future(self) -> FutureSegmentAnythingOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#SegmentAnything
        """
        return super().future  # type: ignore


class TranscribeMedia(CoreNode[TranscribeMediaOut]):
    """https://substrate.run/nodes#TranscribeMedia"""

    def __init__(
        self,
        audio_uri: str,
        prompt: Optional[str] = None,
        language: str = "en",
        segment: bool = False,
        align: bool = False,
        diarize: bool = False,
        suggest_chapters: bool = False,
        hide: bool = False,
    ):
        """
        Args:
            audio_uri: Input audio.
            prompt: Prompt to guide model on the content and context of input audio.
            language: Language of input audio in [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) format.
            segment: Segment the text into sentences with approximate timestamps.
            align: Align transcription to produce more accurate sentence-level timestamps and word-level timestamps. An array of word segments will be included in each sentence segment.
            diarize: Identify speakers for each segment. Speaker IDs will be included in each segment.
            suggest_chapters: Suggest automatic chapter markers.

        https://substrate.run/nodes#TranscribeMedia
        """
        super().__init__(
            audio_uri=audio_uri,
            prompt=prompt,
            language=language,
            segment=segment,
            align=align,
            diarize=diarize,
            suggest_chapters=suggest_chapters,
            hide=hide,
            out_type=TranscribeMediaOut,
        )
        self.node = "TranscribeMedia"

    @property
    def future(self) -> FutureTranscribeMediaOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#TranscribeMedia
        """
        return super().future  # type: ignore


class GenerateSpeech(CoreNode[GenerateSpeechOut]):
    """https://substrate.run/nodes#GenerateSpeech"""

    def __init__(self, text: str, store: Optional[str] = None, hide: bool = False):
        """
        Args:
            text: Input text.
            store: Use "hosted" to return an audio URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the audio data will be returned as a base64-encoded string.

        https://substrate.run/nodes#GenerateSpeech
        """
        super().__init__(text=text, store=store, hide=hide, out_type=GenerateSpeechOut)
        self.node = "GenerateSpeech"

    @property
    def future(self) -> FutureGenerateSpeechOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#GenerateSpeech
        """
        return super().future  # type: ignore


class XTTSV2(CoreNode[XTTSV2Out]):
    """https://substrate.run/nodes#XTTSV2"""

    def __init__(
        self,
        text: str,
        audio_uri: Optional[str] = None,
        language: str = "en",
        store: Optional[str] = None,
        hide: bool = False,
    ):
        """
        Args:
            text: Input text.
            audio_uri: Reference audio used to synthesize the speaker. If unset, a default speaker voice will be used.
            language: Language of input text. Supported languages: `en, de, fr, es, it, pt, pl, zh, ar, cs, ru, nl, tr, hu, ko`.
            store: Use "hosted" to return an audio URL hosted on Substrate. You can also provide a URL to a registered [file store](https://guides.substrate.run/guides/external-file-storage). If unset, the audio data will be returned as a base64-encoded string.

        https://substrate.run/nodes#XTTSV2
        """
        super().__init__(
            text=text,
            audio_uri=audio_uri,
            language=language,
            store=store,
            hide=hide,
            out_type=XTTSV2Out,
        )
        self.node = "XTTSV2"

    @property
    def future(self) -> FutureXTTSV2Out:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#XTTSV2
        """
        return super().future  # type: ignore


class EmbedText(CoreNode[EmbedTextOut]):
    """https://substrate.run/nodes#EmbedText"""

    def __init__(
        self,
        text: str,
        collection_name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedded_metadata_keys: Optional[List[str]] = None,
        doc_id: Optional[str] = None,
        model: Literal["jina-v2", "clip"] = "jina-v2",
        hide: bool = False,
    ):
        """
        Args:
            text: Text to embed.
            collection_name: Vector store name.
            metadata: Metadata that can be used to query the vector store. Ignored if `collection_name` is unset.
            embedded_metadata_keys: Choose keys from `metadata` to embed with text.
            doc_id: Vector store document ID. Ignored if `store` is unset.
            model: Selected embedding model.

        https://substrate.run/nodes#EmbedText
        """
        super().__init__(
            text=text,
            collection_name=collection_name,
            metadata=metadata,
            embedded_metadata_keys=embedded_metadata_keys,
            doc_id=doc_id,
            model=model,
            hide=hide,
            out_type=EmbedTextOut,
        )
        self.node = "EmbedText"

    @property
    def future(self) -> FutureEmbedTextOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#EmbedText
        """
        return super().future  # type: ignore


class MultiEmbedText(CoreNode[MultiEmbedTextOut]):
    """https://substrate.run/nodes#MultiEmbedText"""

    def __init__(
        self,
        items: List[EmbedTextItem],
        collection_name: Optional[str] = None,
        embedded_metadata_keys: Optional[List[str]] = None,
        model: Literal["jina-v2", "clip"] = "jina-v2",
        hide: bool = False,
    ):
        """
        Args:
            items: Items to embed.
            collection_name: Vector store name.
            embedded_metadata_keys: Choose keys from `metadata` to embed with text.
            model: Selected embedding model.

        https://substrate.run/nodes#MultiEmbedText
        """
        super().__init__(
            items=items,
            collection_name=collection_name,
            embedded_metadata_keys=embedded_metadata_keys,
            model=model,
            hide=hide,
            out_type=MultiEmbedTextOut,
        )
        self.node = "MultiEmbedText"

    @property
    def future(self) -> FutureMultiEmbedTextOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#MultiEmbedText
        """
        return super().future  # type: ignore


class JinaV2(CoreNode[JinaV2Out]):
    """https://substrate.run/nodes#JinaV2"""

    def __init__(
        self,
        items: List[EmbedTextItem],
        collection_name: Optional[str] = None,
        embedded_metadata_keys: Optional[List[str]] = None,
        hide: bool = False,
    ):
        """
        Args:
            items: Items to embed.
            collection_name: Vector store name.
            embedded_metadata_keys: Choose keys from `metadata` to embed with text.

        https://substrate.run/nodes#JinaV2
        """
        super().__init__(
            items=items,
            collection_name=collection_name,
            embedded_metadata_keys=embedded_metadata_keys,
            hide=hide,
            out_type=JinaV2Out,
        )
        self.node = "JinaV2"

    @property
    def future(self) -> FutureJinaV2Out:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#JinaV2
        """
        return super().future  # type: ignore


class EmbedImage(CoreNode[EmbedImageOut]):
    """https://substrate.run/nodes#EmbedImage"""

    def __init__(
        self,
        image_uri: str,
        collection_name: Optional[str] = None,
        doc_id: Optional[str] = None,
        model: Literal["clip"] = "clip",
        hide: bool = False,
    ):
        """
        Args:
            image_uri: Image to embed.
            collection_name: Vector store name.
            doc_id: Vector store document ID. Ignored if `collection_name` is unset.
            model: Selected embedding model.

        https://substrate.run/nodes#EmbedImage
        """
        super().__init__(
            image_uri=image_uri,
            collection_name=collection_name,
            doc_id=doc_id,
            model=model,
            hide=hide,
            out_type=EmbedImageOut,
        )
        self.node = "EmbedImage"

    @property
    def future(self) -> FutureEmbedImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#EmbedImage
        """
        return super().future  # type: ignore


class MultiEmbedImage(CoreNode[MultiEmbedImageOut]):
    """https://substrate.run/nodes#MultiEmbedImage"""

    def __init__(
        self,
        items: List[EmbedImageItem],
        collection_name: Optional[str] = None,
        model: Literal["clip"] = "clip",
        hide: bool = False,
    ):
        """
        Args:
            items: Items to embed.
            collection_name: Vector store name.
            model: Selected embedding model.

        https://substrate.run/nodes#MultiEmbedImage
        """
        super().__init__(
            items=items,
            collection_name=collection_name,
            model=model,
            hide=hide,
            out_type=MultiEmbedImageOut,
        )
        self.node = "MultiEmbedImage"

    @property
    def future(self) -> FutureMultiEmbedImageOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#MultiEmbedImage
        """
        return super().future  # type: ignore


class CLIP(CoreNode[CLIPOut]):
    """https://substrate.run/nodes#CLIP"""

    def __init__(
        self,
        items: List[EmbedTextOrImageItem],
        collection_name: Optional[str] = None,
        embedded_metadata_keys: Optional[List[str]] = None,
        hide: bool = False,
    ):
        """
        Args:
            items: Items to embed.
            collection_name: Vector store name.
            embedded_metadata_keys: Choose keys from `metadata` to embed with text. Only applies to text items.

        https://substrate.run/nodes#CLIP
        """
        super().__init__(
            items=items,
            collection_name=collection_name,
            embedded_metadata_keys=embedded_metadata_keys,
            hide=hide,
            out_type=CLIPOut,
        )
        self.node = "CLIP"

    @property
    def future(self) -> FutureCLIPOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#CLIP
        """
        return super().future  # type: ignore


class CreateVectorStore(CoreNode[CreateVectorStoreOut]):
    """https://substrate.run/nodes#CreateVectorStore"""

    def __init__(
        self,
        collection_name: str,
        model: Literal["jina-v2", "clip"],
        m: int = 16,
        ef_construction: int = 64,
        metric: Literal["cosine", "l2", "inner"] = "inner",
        hide: bool = False,
    ):
        """
        Args:
            collection_name: Vector store name.
            model: Selected embedding model.
            m: The max number of connections per layer for the index.
            ef_construction: The size of the dynamic candidate list for constructing the index graph.
            metric: The distance metric to construct the index with.

        https://substrate.run/nodes#CreateVectorStore
        """
        super().__init__(
            collection_name=collection_name,
            model=model,
            m=m,
            ef_construction=ef_construction,
            metric=metric,
            hide=hide,
            out_type=CreateVectorStoreOut,
        )
        self.node = "CreateVectorStore"

    @property
    def future(self) -> FutureCreateVectorStoreOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#CreateVectorStore
        """
        return super().future  # type: ignore


class ListVectorStores(CoreNode[ListVectorStoresOut]):
    """https://substrate.run/nodes#ListVectorStores"""

    def __init__(self, hide: bool = False):
        """
        Args:

        https://substrate.run/nodes#ListVectorStores
        """
        super().__init__(hide=hide, out_type=ListVectorStoresOut)
        self.node = "ListVectorStores"

    @property
    def future(self) -> FutureListVectorStoresOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#ListVectorStores
        """
        return super().future  # type: ignore


class DeleteVectorStore(CoreNode[DeleteVectorStoreOut]):
    """https://substrate.run/nodes#DeleteVectorStore"""

    def __init__(
        self,
        collection_name: str,
        model: Literal["jina-v2", "clip"],
        hide: bool = False,
    ):
        """
        Args:
            collection_name: Vector store name.
            model: Selected embedding model.

        https://substrate.run/nodes#DeleteVectorStore
        """
        super().__init__(
            collection_name=collection_name,
            model=model,
            hide=hide,
            out_type=DeleteVectorStoreOut,
        )
        self.node = "DeleteVectorStore"

    @property
    def future(self) -> FutureDeleteVectorStoreOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#DeleteVectorStore
        """
        return super().future  # type: ignore


class FetchVectors(CoreNode[FetchVectorsOut]):
    """https://substrate.run/nodes#FetchVectors"""

    def __init__(
        self,
        collection_name: str,
        model: Literal["jina-v2", "clip"],
        ids: List[str],
        hide: bool = False,
    ):
        """
        Args:
            collection_name: Vector store name.
            model: Selected embedding model.
            ids: Document IDs to retrieve.

        https://substrate.run/nodes#FetchVectors
        """
        super().__init__(
            collection_name=collection_name,
            model=model,
            ids=ids,
            hide=hide,
            out_type=FetchVectorsOut,
        )
        self.node = "FetchVectors"

    @property
    def future(self) -> FutureFetchVectorsOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#FetchVectors
        """
        return super().future  # type: ignore


class UpdateVectors(CoreNode[UpdateVectorsOut]):
    """https://substrate.run/nodes#UpdateVectors"""

    def __init__(
        self,
        collection_name: str,
        model: Literal["jina-v2", "clip"],
        vectors: List[UpdateVectorParams],
        hide: bool = False,
    ):
        """
        Args:
            collection_name: Vector store name.
            model: Selected embedding model.
            vectors: Vectors to upsert.

        https://substrate.run/nodes#UpdateVectors
        """
        super().__init__(
            collection_name=collection_name,
            model=model,
            vectors=vectors,
            hide=hide,
            out_type=UpdateVectorsOut,
        )
        self.node = "UpdateVectors"

    @property
    def future(self) -> FutureUpdateVectorsOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#UpdateVectors
        """
        return super().future  # type: ignore


class DeleteVectors(CoreNode[DeleteVectorsOut]):
    """https://substrate.run/nodes#DeleteVectors"""

    def __init__(
        self,
        collection_name: str,
        model: Literal["jina-v2", "clip"],
        ids: List[str],
        hide: bool = False,
    ):
        """
        Args:
            collection_name: Vector store name.
            model: Selected embedding model.
            ids: Document IDs to delete.

        https://substrate.run/nodes#DeleteVectors
        """
        super().__init__(
            collection_name=collection_name,
            model=model,
            ids=ids,
            hide=hide,
            out_type=DeleteVectorsOut,
        )
        self.node = "DeleteVectors"

    @property
    def future(self) -> FutureDeleteVectorsOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#DeleteVectors
        """
        return super().future  # type: ignore


class QueryVectorStore(CoreNode[QueryVectorStoreOut]):
    """https://substrate.run/nodes#QueryVectorStore"""

    def __init__(
        self,
        collection_name: str,
        model: Literal["jina-v2", "clip"],
        query_strings: Optional[List[str]] = None,
        query_image_uris: Optional[List[str]] = None,
        query_vectors: Optional[List[List[float]]] = None,
        query_ids: Optional[List[str]] = None,
        top_k: int = 10,
        ef_search: int = 40,
        include_values: bool = False,
        include_metadata: bool = False,
        filters: Optional[Dict[str, Any]] = None,
        hide: bool = False,
    ):
        """
        Args:
            collection_name: Vector store to query against.
            model: Selected embedding model.
            query_strings: Texts to embed and use for the query.
            query_image_uris: Image URIs to embed and use for the query.
            query_vectors: Vectors to use for the query.
            query_ids: Document IDs to use for the query.
            top_k: Number of results to return.
            ef_search: The size of the dynamic candidate list for searching the index graph.
            include_values: Include the values of the vectors in the response.
            include_metadata: Include the metadata of the vectors in the response.
            filters: Filter metadata by key-value pairs.

        https://substrate.run/nodes#QueryVectorStore
        """
        super().__init__(
            collection_name=collection_name,
            model=model,
            query_strings=query_strings,
            query_image_uris=query_image_uris,
            query_vectors=query_vectors,
            query_ids=query_ids,
            top_k=top_k,
            ef_search=ef_search,
            include_values=include_values,
            include_metadata=include_metadata,
            filters=filters,
            hide=hide,
            out_type=QueryVectorStoreOut,
        )
        self.node = "QueryVectorStore"

    @property
    def future(self) -> FutureQueryVectorStoreOut:  # type: ignore
        """
        Future reference to this node's output.

        https://substrate.run/nodes#QueryVectorStore
        """
        return super().future  # type: ignore
