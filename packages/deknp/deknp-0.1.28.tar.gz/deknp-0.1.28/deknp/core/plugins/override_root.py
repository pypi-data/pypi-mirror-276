import os
import tempfile
from distutils.dir_util import copy_tree
from dektools.file.operation import write_file
from dekgen.tmpl.template import Template
from .base import Plugin


class PluginOverrideRootTemplate(Template):
    file_ignore_name = 'dek-override'


class PluginOverrideRoot(Plugin):
    template_cls = PluginOverrideRootTemplate

    override_key = 'override'
    dek_overrides_dir_name = 'dek-override'

    def run(self):
        ignore_info = self.merge_from_key(self.override_key)
        dir_temp = tempfile.mkdtemp()
        dir_temp_final = os.path.join(dir_temp, 'final')
        os.makedirs(dir_temp_final)
        for i, dir_dek in enumerate(self.dek_dir_list):
            dir_target = os.path.join(dir_temp, str(i))
            src = os.path.join(dir_dek, self.dek_overrides_dir_name)
            if os.path.exists(src):
                os.makedirs(dir_target)
                self.template_full.render_dir(dir_target, src, open_ignore_override=False)
        for x in os.listdir(dir_temp):
            path = os.path.join(dir_temp, x)
            if path != dir_temp_final:
                copy_tree(path, dir_temp_final)
        for filename, info in ignore_info.items():
            write_file(
                os.path.join(dir_temp_final, self.template_cls.get_file_ignore(filename)),
                s="\n".join([x for x, b in info.items() if b])
            )
        self.template_full.render_dir(self.project_dir, dir_temp_final, force_close_tpl=True)
