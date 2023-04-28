
def get_upload_path(instance, filename):
    return f"{str(instance.pk)}/{filename}/"