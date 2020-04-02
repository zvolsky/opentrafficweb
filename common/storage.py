from whitenoise.storage import CompressedManifestStaticFilesStorage


# https://stackoverflow.com/questions/44160666/valueerror-missing-staticfiles-manifest-entry-for-favicon-ico
class WhitenoiseCompressedManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False
