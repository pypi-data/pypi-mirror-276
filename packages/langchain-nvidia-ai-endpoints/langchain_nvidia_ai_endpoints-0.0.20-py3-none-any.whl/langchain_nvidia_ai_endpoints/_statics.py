from typing import Optional

from langchain_core.pydantic_v1 import BaseModel


class Model(BaseModel):
    id: str
    model_type: Optional[str] = None
    api_type: Optional[str] = None
    model_name: Optional[str] = None
    client: Optional[str] = None
    path: str


MODEL_SPECS = {
    "playground_smaug_72b": {"model_type": "chat", "api_type": "aifm"},
    "playground_kosmos_2": {
        "model_type": "image_in",
        "api_type": "aifm",
        "alternative": "microsoft/kosmos-2",
    },
    "playground_llama2_70b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "meta/llama2-70b",
    },
    "playground_gemma_7b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "google/gemma-7b",
    },
    "playground_mistral_7b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "mistralai/mistral-7b-instruct-v0.2",
    },
    "playground_mamba_chat": {"model_type": "chat", "api_type": "aifm"},
    "playground_phi2": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "microsoft/phi-3-mini-128k-instruct",
    },
    "playground_sdxl": {"model_type": "image_out", "api_type": "aifm"},
    "playground_nv_llama2_rlhf_70b": {"model_type": "chat", "api_type": "aifm"},
    "playground_neva_22b": {
        "model_type": "image_in",
        "api_type": "aifm",
        "alternative": "nvidia/neva-22b",
    },
    "playground_yi_34b": {"model_type": "chat", "api_type": "aifm"},
    "playground_nemotron_steerlm_8b": {"model_type": "chat", "api_type": "aifm"},
    "playground_cuopt": {"model_type": "cuopt", "api_type": "aifm"},
    "playground_llama_guard": {"model_type": "classifier", "api_type": "aifm"},
    "playground_starcoder2_15b": {"model_type": "completion", "api_type": "aifm"},
    "playground_deplot": {
        "model_type": "image_in",
        "api_type": "aifm",
        "alternative": "google/deplot",
    },
    "playground_llama2_code_70b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "meta/codelama-70b",
    },
    "playground_gemma_2b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "google/gemma-2b",
    },
    "playground_seamless": {"model_type": "translation", "api_type": "aifm"},
    "playground_mixtral_8x7b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "mistralai/mixtral-8x7b-instruct-v0.1",
    },
    "playground_fuyu_8b": {
        "model_type": "image_in",
        "api_type": "aifm",
        "alternative": "adept/fuyu-8b",
    },
    "playground_llama2_code_34b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "meta/codellama-70b",
    },
    "playground_llama2_code_13b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "meta/codellama-70b",
    },
    "playground_steerlm_llama_70b": {"model_type": "chat", "api_type": "aifm"},
    "playground_clip": {"model_type": "similarity", "api_type": "aifm"},
    "playground_llama2_13b": {
        "model_type": "chat",
        "api_type": "aifm",
        "alternative": "meta/llama2-70b",
    },
}

MODEL_SPECS.update(
    {
        "ai-codellama-70b": {"model_type": "chat", "model_name": "meta/codellama-70b"},
        "ai-embed-qa-4": {"model_type": "embedding", "model_name": "NV-Embed-QA"},
        "ai-fuyu-8b": {"model_type": "image_in", "model_name": "adept/fuyu-8b"},
        "ai-gemma-7b": {"model_type": "chat", "model_name": "google/gemma-7b"},
        "ai-google-deplot": {"model_type": "image_in", "model_name": "google/deplot"},
        "ai-llama2-70b": {"model_type": "chat", "model_name": "meta/llama2-70b"},
        "ai-microsoft-kosmos-2": {
            "model_type": "image_in",
            "model_name": "microsoft/kosmos-2",
        },
        "ai-mistral-7b-instruct-v2": {
            "model_type": "chat",
            "model_name": "mistralai/mistral-7b-instruct-v0.2",
        },
        "ai-mixtral-8x7b-instruct": {
            "model_type": "chat",
            "model_name": "mistralai/mixtral-8x7b-instruct-v0.1",
        },
        "ai-neva-22b": {"model_type": "image_in", "model_name": "nvidia/neva-22b"},
        "ai-rerank-qa-mistral-4b": {
            "model_type": "ranking",
            "model_name": "nv-rerank-qa-mistral-4b:1",  # nvidia/rerank-qa-mistral-4b
        },
        # 'ai-sdxl-turbo': {'model_type': 'image_out'},
        # 'ai-stable-diffusion-xl-base': {'model_type': 'iamge_out'},
        "ai-codegemma-7b": {"model_type": "chat", "model_name": "google/codegemma-7b"},
        "ai-recurrentgemma-2b": {
            "model_type": "chat",
            "model_name": "google/recurrentgemma-2b",
        },
        "ai-gemma-2b": {"model_type": "chat", "model_name": "google/gemma-2b"},
        "ai-mistral-large": {
            "model_type": "chat",
            "model_name": "mistralai/mistral-large",
        },
        "ai-mixtral-8x22b": {
            "model_type": "completion",
            "model_name": "mistralai/mixtral-8x22b-v0.1",
        },
        "ai-mixtral-8x22b-instruct": {
            "model_type": "chat",
            "model_name": "mistralai/mixtral-8x22b-instruct-v0.1",
        },
        "ai-llama3-8b": {"model_type": "chat", "model_name": "meta/llama3-8b-instruct"},
        "ai-llama3-70b": {
            "model_type": "chat",
            "model_name": "meta/llama3-70b-instruct",
        },
        "ai-phi-3-mini": {
            "model_type": "chat",
            "model_name": "microsoft/phi-3-mini-128k-instruct",
        },
        "ai-arctic": {"model_type": "chat", "model_name": "snowflake/arctic"},
        "ai-dbrx-instruct": {
            "model_type": "chat",
            "model_name": "databricks/dbrx-instruct",
        },
        "ai-phi-3-mini-4k": {
            "model_type": "chat",
            "model_name": "microsoft/phi-3-mini-4k-instruct",
        },
        "ai-seallm-7b": {"model_type": "chat", "model_name": "seallms/seallm-7b-v2.5"},
        "ai-sea-lion-7b-instruct": {
            "model_type": "chat",
            "model_name": "aisingapore/sea-lion-7b-instruct",
        },
        "ai-google-paligemma": {
            "model_type": "image_in",
            "model_name": "google/paligemma",
        },
        "ai-arctic-embed-l": {
            "model_type": "embedding",
            "model_name": "snowflake/arctic-embed-l",
        },
        "ai-phi-3-small-8k-instruct": {
            "model_type": "chat",
            "model_name": "microsoft/phi-3-small-8k-instruct",
        },
        "ai-phi-3-small-128k-instruct": {
            "model_type": "chat",
            "model_name": "microsoft/phi-3-small-128k-instruct",
        },
        "ai-phi-3-medium-4k-instruct": {
            "model_type": "chat",
            "model_name": "microsoft/phi-3-medium-4k-instruct",
        },
        "ai-phi-3-vision-128k-instruct": {
            "model_type": "image_in",
            "model_name": "microsoft/phi-3-vision-128k-instruct",
        },
        "ai-granite-8b-code-instruct": {
            "model_type": "chat",
            "model_name": "ibm/granite-8b-code-instruct",
        },
        "ai-granite-34b-code-instruct": {
            "model_type": "chat",
            "model_name": "ibm/granite-34b-code-instruct",
        },
        "ai-codegemma-1-1-7b": {
            "model_type": "chat",
            "model_name": "google/codegemma-1.1-7b",
        },
    }
)

client_map = {
    "asr": "None",
    "chat": "ChatNVIDIA",
    "classifier": "None",
    "completion": "NVIDIA",
    "cuopt": "None",
    "embedding": "NVIDIAEmbeddings",
    "image_in": "ChatNVIDIA",
    "image_out": "ImageGenNVIDIA",
    "qa": "ChatNVIDIA",
    "similarity": "None",
    "translation": "None",
    "tts": "None",
    "ranking": "NVIDIARerank",
}

MODEL_SPECS = {
    k: {**v, "client": client_map[v["model_type"]]} for k, v in MODEL_SPECS.items()
}
# MODEL_SPEC database should have both function and model names
MODEL_SPECS.update(
    {v["model_name"]: v for v in MODEL_SPECS.values() if "model_name" in v}
)
