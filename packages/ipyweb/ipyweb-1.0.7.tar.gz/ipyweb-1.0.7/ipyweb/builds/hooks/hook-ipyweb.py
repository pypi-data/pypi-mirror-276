from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from ipyweb.builds.builder import builder

datas = []
hiddenimports = builder.getHiddenImports(False)
 
def hook(pyi_config):
    return datas, hiddenimports
