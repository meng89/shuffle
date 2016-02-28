import sys
import os

dir_ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_)
sys.path.insert(0, os.path.abspath(os.path.join(dir_, "..")))

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

import ipodshuffle
import ipodshuffle.shuffle
import ipodshuffle.version

extensions = ['sphinx.ext.autodoc']
extensions += ['sphinxcontrib.programoutput']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'ipodshuffle'
copyright = u'2016, Chen Meng'
author = u'Chen Meng'


version = ipodshuffle.version.__version__
release = ipodshuffle.version.__version__

language = None

exclude_patterns = ['_build']

pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

html_static_path = ['_static']

htmlhelp_basename = 'ipodshuffledoc'

man_pages = [
    (master_doc, 'ipodshuffle', u'ipodshuffle Documentation',
     [author], 1)
]

texinfo_documents = [
  (master_doc, 'ipodshuffle', u'ipodshuffle Documentation',
   author, 'ipodshuffle', 'One line description of project.',
   'Miscellaneous'),
]

autoclass_content = 'both'
autodoc_member_order = 'bysource'
