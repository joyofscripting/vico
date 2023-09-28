import os
import json
import platform
from pathlib import Path
from teksto import TransformSettings, TransformSettingsPreset


class VicoPreferences(object):
    """
    Manages the user preferences of vico.

    Attributes:
        selected_preset_index (int): Index of the selected preset in the listbox.
        presets (:obj:`list` of :obj:`TransformSettingsPreset`): Exception error code.
    """
    def __init__(self):
        """
        Initializes a new instance of the user preferences and tries to load existing preferences
        from a JSON file. If the file does not exist default preferences are used.
        """
        self._selected_preset_index = None
        self._presets = None
        self._prefs_filepath = VicoPreferences._find_prefs_filepath()

        self.load()

    @staticmethod
    def _find_prefs_filepath():
        """
        Returns the path of the file where the user preferences are saved.
        """
        current_platform = platform.system()

        if current_platform == 'Windows':
            prefs_filepath = os.path.expandvars("%appdata%/vico/vico_settings.json")
        elif current_platform == 'Darwin':
            prefs_filepath = os.path.expanduser("~/Library/Preferences/vico_settings.json")
        elif current_platform == 'Linux':
            prefs_filepath = os.path.expanduser("~/.config/vico_settings.json")
        else:
            prefs_filepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'vico_settings.json')

        return prefs_filepath

    @property
    def selected_preset_index(self):
        return self._selected_preset_index

    @selected_preset_index.setter
    def selected_preset_index(self, selected_preset_index):
        self._selected_preset_index = selected_preset_index

    @property
    def presets(self):
        return self._presets

    @presets.setter
    def presets(self, presets):
        self._presets = presets

    @property
    def prefs_filepath(self):
        return self._prefs_filepath

    @prefs_filepath.setter
    def prefs_filepath(self, prefs_filepath):
        self._prefs_filepath = prefs_filepath

    @property
    def selected_transform_settings(self):
        return self.presets[self.selected_preset_index].transform_settings

    @property
    def selected_preset(self):
        return self.presets[self.selected_preset_index]

    def load(self):
        """
        Loads the user preferences from the JSON file. If the file does not exist default preferences are used.
        """
        try:
            with open(self.prefs_filepath, "r") as prefs_file:
                json_data = json.load(prefs_file)
        except FileNotFoundError:
            json_data = None

        if json_data:
            presets = []
            for preset in json_data['presets']:
                tsp = TransformSettingsPreset.from_dict(preset)
                presets.append(tsp)
            selected_preset_idx = json_data['selected_preset_index']
        else:
            prefix, suffix, delimiter = "'", "'", ","
            line_up = False
            quote_text = False
            ts = TransformSettings(prefix=prefix, suffix=suffix, delimiter=delimiter, line_up=line_up,
                                   quote_text=quote_text)
            presets = [TransformSettingsPreset('Default', ts)]
            selected_preset_idx = 0

        self.selected_preset_index = selected_preset_idx
        self.presets = presets

    def save(self):
        """
        Saves the current user preferences to a JSON file.
        """
        prefs_dict = {'selected_preset_index': self.selected_preset_index,
                      'presets': [preset.to_dict() for preset in self.presets]}
        
        output_file = Path(self.prefs_filepath)
        output_file.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_file, "w") as prefs_file:
            json.dump(prefs_dict, prefs_file, indent=4)
