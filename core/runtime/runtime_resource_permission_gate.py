class RuntimeResourcePermissionGate:
    """
    Controls all external resource acquisition.
    NOTHING downloads or installs without passing here.
    """

    def __init__(self):
        self.allowed = set()
        self.denied = set()

    def request(self, resource, reason="unknown"):
        return {
            "resource": resource,
            "approved": False,
            "reason": reason,
            "requires_user_approval": True
        }

    def approve(self, resource):
        self.allowed.add(resource)
        return True

    def deny(self, resource):
        self.denied.add(resource)
        return False

    def can_fetch(self, resource):
        return resource in self.allowed