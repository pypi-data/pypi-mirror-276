from kabaret import flow
from kabaret.flow.object import _Manager
from  libreflow.baseflow.asset import AssetFamily, Asset

import gazu
import subprocess
import os
import sys

#
# C:\Users\flavio\Desktop\dev\env-test-anpo
#
# /anpo/asset_types/sets/asset_families/sq015     ->  2680
# 

def log(msg, lvl):
    old_stdout = sys.stdout
    sys.stdout = sys.__stdout__
    print(f"[EXPORT LAYERS] {lvl.ljust(8)} - {msg}")
    sys.stdout = old_stdout

def log_info(msg):
    return log(msg, "INFO")

def log_warning(msg):
    return log(msg, "WARNING")

def log_error(msg):
    return log(msg, "ERROR")

def create_revision(_file, name):
    comment = ""
    status = "Available"

    rev = _file.add_revision(name, comment=comment)
    rev.set_sync_status(status)

    return rev.get_path()





class ExportIllustratorLayers(flow.Action):
    _MANAGER_TYPE = _Manager
    parent = flow.Parent()

    def get_project_id(self):
        return self.root().project().kitsu_config().project_id.get()

    def get_project_root_folder(self):
        return self.root().project().get_root()

    def get_gazu(self):
        return self.root().project().kitsu_api()
    
    def get_illustrator_path(self):
        _envs = self.root().project().get_current_site().site_environment
        return _envs["ILLUSTRATOR_EXEC_PATH"].value.get() if "ILLUSTRATOR_EXEC_PATH" in _envs.mapped_names() else None
    
    def get_illustrator_script(self):
        path = os.path.join(os.path.dirname(__file__), "scripts", "layers2png.jsx")
        if not os.path.exists(path):
            print('ERROR : COULD NOT FIND THE ILLUSTRATOR SCRIPT @:')
            print(path)
        return path
    
    def create_layers(self, assets):
        ai_files_list = []
        
        #assets = self.assets
        print(assets)
        
        for a in assets:
            
            bg_code = a.get_code()
            
            print(a.name())
            tasks = a.tasks
            if tasks.has_mapped_name('design') is False:
                print(f'Set {a.name()} don\'t have a design task')
                continue
            try:
                ai_file = self.root().get_object(a.oid()+"/tasks/design/files/design_ai")
            except:
                log_warning(f"{a.name()}: has no design.ai")
                continue
            rev = ai_file.get_head_revision(sync_status='Available')
            if rev is None:
                log_warning(f"{a.name()}: layout not started yet (no published version)")
                continue
            elif not os.path.isfile(rev.get_path()):
                log_warning(f"{a.name()}: design.ai revision {rev.name()} doesn't exist on file system")
                continue
            print("ok")
            
            rev_name = rev.name()
            print(rev_name)
            
            task = tasks['design']
            if task.files.has_mapped_name("layers") is False:
                task.create_dft_files.files.update() # update action default files
                task.create_dft_files.run('Create')        
            
            layers = task.files['layers']
            if layers.has_revision(rev_name):
                log_warning(f"{a.name()}: layers revision {rev.name()} already exists")
            else:
                rev_path = create_revision(layers, rev_name)
            ai_files_list.append(rev.get_path())
            
        
        os.environ["LIBREFLOW_AI2LAYERS_AILIST"] = ";".join(ai_files_list).replace("\\", "/")
        os.environ["LIBREFLOW_ROOT_FOLDER"] = self.get_project_root_folder().replace("\\", "/")
        if not ai_files_list:
            print("No AI Files to Process in this selection")
        else: 
            script_path = self.get_illustrator_script()
            if not script_path:
                print("script jsx was not found... stopping action now")
                return
            
            _run = subprocess.run([self.get_illustrator_path(), "/run", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(_run.stderr)
            print(_run.stdout)

    def select_assets(self):
        return self.parent.assets.mapped_items() 

    def needs_dialog(self):
        return False
    

    def run(self, button):
        asset_list = self.select_assets()
        print(asset_list)
        if asset_list:
            self.create_layers(asset_list)
        else:
            print("NO ASSET PROVIDED, NOTHING TO EXPORT")

class ExportIllustratorLayersAssetFamily(ExportIllustratorLayers):
    pass

class ExportIllustratorLayersAssets(ExportIllustratorLayers):
    def select_assets(self):
        return [self.parent]


from . import _version
__version__ = _version.get_versions()['version']


def create_action_ExportIllustratorLayersAssets(parent):
    if isinstance(parent, Asset) and parent.oid().startswith("/anpo/asset_types/sets/asset_families/sq"):
        r = flow.Child(ExportIllustratorLayersAssets)
        r.name = 'export_layers'
        return r



def create_action_ExportIllustratorLayersAssetFamily(parent):
    if isinstance(parent, AssetFamily) and parent.oid().startswith("/anpo/asset_types/sets"):
        r = flow.Child(ExportIllustratorLayersAssetFamily)
        r.name = 'export_layers'
        return r


def install_extensions(session):
    return {
        "demo": [
            create_action_ExportIllustratorLayersAssetFamily,
            create_action_ExportIllustratorLayersAssets,
        ]
    }


