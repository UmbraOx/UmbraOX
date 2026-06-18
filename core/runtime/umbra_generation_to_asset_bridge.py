from core.runtime.umbra_asset import UmbraAsset


class UmbraGenerationToAssetBridge:
    """
    Converts raw generation outputs into persistent Umbra assets.
    """

    def __init__(self, asset_store):

        self.asset_store = asset_store

    def convert(self, task_type: str, generation_result: dict) -> UmbraAsset:

        asset = UmbraAsset(
            asset_type=task_type,
            data=generation_result,
            metadata={
                "source": "generation_engine",
                "auto_converted": True
            }
        )

        return self.asset_store.save(asset)