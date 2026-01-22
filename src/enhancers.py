import os
import numpy as np

class PassthroughEnhancer:
    name = "passthrough"

    def process(self, x: np.ndarray, sample_rate: int) -> np.ndarray:
        # x: shape (frames,), float32
        return x

def get_enhancer():
    """
    Returns an enhancer object with a uniform .process(x, sample_rate) API.
    If AIC_SDK_KEY is present, you can later swap in ai-coustics here.
    """
    key = os.getenv("AIC_SDK_KEY")
    if not key:
        return PassthroughEnhancer()

    # TODO: Replace with real ai-coustics enhancer when you get a key + model id.
    # from aic_sdk import ...
    # return AicousticsEnhancer(key=key, model_id=os.getenv("AIC_MODEL_ID"))
    return PassthroughEnhancer()
