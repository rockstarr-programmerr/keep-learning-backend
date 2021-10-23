from storages.backends.s3boto3 import S3StaticStorage


class ExerciseImageStorage(S3StaticStorage):
    """
    Because image URL is saved in html by CKEditor, we must use S3StaticStorage
    so that `querystring_auth` is disabled, and URL is always the same.
    Also, set `default_acl` to 'public-read' so that these images are accessible.
    """
    default_acl = 'public-read'
