from util import extract_text_between_markers

from ._version import __version__  # noqa

# use readme in pydoc
__doc__ = extract_text_between_markers(file_path="README.md", start="docs_start", stop="docs_stop")
