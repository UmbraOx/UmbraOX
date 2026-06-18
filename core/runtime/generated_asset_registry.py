class GeneratedAssetRegistry:

    def __init__(self):

        self.assets = []

    def register(
        self,
        asset
    ):

        self.assets.append(asset)

    def all(self):

        return self.assets