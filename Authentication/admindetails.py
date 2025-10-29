from Model.admin_model import AdminModel

def ReadFile_fromJson():
    """Helper function to maintain backward compatibility."""
    return AdminModel().read_admins()
