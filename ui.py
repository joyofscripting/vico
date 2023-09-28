import PySimpleGUI as sg
import pyperclip
from teksto import TransformSettings, TransformSettingsPreset, TextTransformer, TextTransformerError

MOVE_DIRECTION_UP = 'UP'
MOVE_DIRECTION_DOWN = 'DOWN'


def prepare_main_window(window_title, prefs):
    """
    Prepares the main window before it is shown for the first time after startup.

    Args:
        window_title (str): The title to be shown in the main window.
        prefs (:obj:`VicoPreferences`): The user preferences necessary to initialize UI elements.

    Returns:
        The prepared main window.
    """
    clipboard_content = pyperclip.paste()

    # Frame layout for the "Text input" frame
    fl_text_input = [
        [sg.Multiline(clipboard_content, size=(60, 8), key='fld_clipboard_content', enable_events=True)],
        [sg.Button('Copy from clipboard', key='btn_copy_from_clipboard'),
         sg.Button('Clear', key='btn_clear_text_input'),
         sg.Text('', key='txt_input_count_lines')]
    ]

    # Frame layout for the "Transform options" frame
    fl_transform_options = [
        [sg.Text('Prefix', size=(9, 1)),
         sg.InputText(default_text=prefs.selected_transform_settings.prefix,
                      key='prefix',
                      size=(5, 1)),
         sg.Checkbox('Line up', default=prefs.selected_transform_settings.line_up, key='chk_line_up')],
        [sg.Text('Suffix', size=(9, 1)),
         sg.InputText(default_text=prefs.selected_transform_settings.suffix,
                      key='suffix', size=(5, 1)),
         sg.Checkbox('Quote text',
                     default=prefs.selected_transform_settings.quote_text,
                     key='chk_quote_text',
                     enable_events=True)],
        [sg.Text('Delimiter', size=(9, 1)),
         sg.InputText(default_text=prefs.selected_transform_settings.delimiter,
                      key='delimiter', size=(5, 1)),
         sg.Text('Quote char'), sg.InputText(default_text=prefs.selected_transform_settings.quote_char,
                                             size=(5, 1),
                                             key='fld_quote_char'),
         sg.Text('Escape char'), sg.InputText(default_text=prefs.selected_transform_settings.escape_char,
                                              size=(5, 1),
                                              key='fld_escape_char')
         ],
        [sg.Text('Surrounding text')],
        [sg.Multiline('', size=(55, 3), key='fld_surrounding_text')]
    ]

    # Frame layout for the "Presets" frame
    fl_presets = [
        [sg.Listbox(values=prefs.presets, size=(30, 6), key='lbx_presets',
                    enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_BROWSE),
         sg.Button('⬆', key='btn_move_preset_up'),
         sg.Button('⬇', key='btn_move_preset_down')],
        [sg.Button('Add', key='btn_add_preset'), sg.Button('Save', key='btn_save_preset'),
         sg.Button('Delete', key='btn_del_preset')]
    ]

    # Frame layout for the "Preview output" frame
    fl_preview_output = [
        [sg.Multiline('', size=(60, 8), key='fld_preview')],
        [sg.Button('Preview', key='btn_preview'),
         sg.Button('Copy to clipboard', key='btn_copy_to_clipboard', disabled=True),
         sg.Text('', key='txt_prv_count_lines')]
    ]

    # Final layout for the main window
    layout = [
        [sg.Frame('Text input', fl_text_input)],
        [sg.Frame('Transform options', fl_transform_options)],
        [sg.Frame('Presets', fl_presets)],
        [sg.Frame('Preview output', fl_preview_output)]
    ]

    window = sg.Window(window_title, layout, enable_close_attempted_event=True, finalize=True)
    # Updating the listbox with the presets to highlight the preset
    # that was chosen when vico was closed the last time.
    window['lbx_presets'].update(set_to_index=prefs.selected_preset_index,
                                 scroll_to_index=prefs.selected_preset_index)
    # Updating the UI to display the values of the chosen preset
    update_displayed_preset(window, prefs.selected_preset)
    # Updating the label showing the count of lines in the text input field
    update_count_lines(window, clipboard_content)

    return window


def clicked_copy_from_clipboard(window):
    """
    Fills the text input field of the "Text input" frame with the content of the clipboard.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
    """
    clipboard_content = pyperclip.paste()
    window['fld_clipboard_content'].update(clipboard_content)
    update_count_lines(window, clipboard_content)


def clicked_clear_text_input(window):
    """
    Clears the text input field of the "Text input" frame.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
    """
    window['fld_clipboard_content'].update('')
    update_count_lines(window, '')


def update_count_lines(window, text):
    """
    Updates the label showing the count of lines of the input text.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        text (str): The input text.
    """
    count_text_lines = get_count_text_lines(text)
    txt_count_lines = "Input contains {0} line(s)".format(count_text_lines)
    window['txt_input_count_lines'].update(txt_count_lines)


def clicked_quote_text_checkbox(values, window):
    """
    Enables or disables the text fields for the quote and escape char
    when the user clicked the "Quote text" checkbox.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        values (dict): The values dictionary returned by the windows.read() method.
    """
    if values['chk_quote_text']:
        window['fld_quote_char'].update(disabled=False)
        window['fld_escape_char'].update(disabled=False)
    else:
        window['fld_quote_char'].update(disabled=True)
        window['fld_escape_char'].update(disabled=True)


def clicked_preset_item(window, values):
    """
    Updates the displayed transform settings according to the selected preset.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        values (dict): The values dictionary returned by the windows.read() method.
    """
    chosen_tsp = values['lbx_presets'][0]
    update_displayed_preset(window, chosen_tsp)


def clicked_add_preset(window):
    """
    Lets the user add a new preset.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
    """
    new_tsp = show_dialog_add_preset()
    # User clicked on the "Save" button in the modal dialog
    if new_tsp:
        lbx_items = window['lbx_presets'].get_list_values()
        lbx_items.append(new_tsp)
        update_preset_listbox(window, lbx_items, len(lbx_items) - 1)
        update_displayed_preset(window, new_tsp)


def clicked_save_preset(window, values):
    """
    Lets the user save the current transform settings to the selected preset.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        values (dict): The values dictionary returned by the windows.read() method.
    """
    selected_idx = window['lbx_presets'].get_indexes()[0]
    lbx_items = window['lbx_presets'].get_list_values()
    chosen_tsp = lbx_items[selected_idx]
    current_ts = get_transform_settings(values)
    chosen_tsp.transform_settings = current_ts


def clicked_delete_preset(window):
    """
    Lets the user delete the selected preset.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
    """
    selected_idx = window['lbx_presets'].get_indexes()[0]
    lbx_items = window['lbx_presets'].get_list_values()
    chosen_tsp = lbx_items[selected_idx]
    if not chosen_tsp.name == 'Default':
        del (lbx_items[selected_idx])
        update_preset_listbox(window, lbx_items, selected_idx - 1)
        update_displayed_preset(window, lbx_items[selected_idx - 1])


def is_valid_up_movement(direction, index):
    """
    Indicates if the given choice is a valid up movement.

    Args:
        direction (str): "UP" or "DOWN" (better use MOVE_DIRECTION_UP or MOVE_DIRECTION_DOWN)
        index (int): The index of the currently selected preset

    Returns:
        Returns True if the direction equals MOVE_DIRECTION_UP and the index is not equal to 0.
        Otherwise, it returns False.
    """
    if direction == MOVE_DIRECTION_UP and index != 0:
        return True
    else:
        return False


def is_valid_down_movement(direction, index, items):
    """
    Indicates if the given choice is a valid down movement.

    Args:
        direction (str): "UP" or "DOWN" (better use MOVE_DIRECTION_UP or MOVE_DIRECTION_DOWN)
        index (int): The index of the currently selected preset
        items (:obj:`list`): The current list represented by the listbox.

    Returns:
        Returns True if the direction equals MOVE_DIRECTION_DOWN and the index is smaller
        than the length of items minus 1.
        Otherwise, it returns False.
    """
    if direction == MOVE_DIRECTION_DOWN and index < len(items) - 1:
        return True
    else:
        return False


def move_selected_preset(window, direction):
    """
    Moves the selected preset up or down in the listbox.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.:
        direction (str): "UP" or "DOWN" (better use MOVE_DIRECTION_UP or MOVE_DIRECTION_DOWN)
    """
    selected_idx = window['lbx_presets'].get_indexes()[0]
    lbx_items = window['lbx_presets'].get_list_values()
    if is_valid_up_movement(direction, selected_idx) or is_valid_down_movement(direction, selected_idx, lbx_items):
        if direction == MOVE_DIRECTION_UP:
            new_index = selected_idx - 1
        elif direction == MOVE_DIRECTION_DOWN:
            new_index = selected_idx + 1

        lbx_items.insert(new_index, lbx_items.pop(selected_idx))
        update_preset_listbox(window, lbx_items, new_index)


def clicked_show_preview(window, values):
    """
    Lets the user preview the result of the text transformation.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        values (dict): The values dictionary returned by the windows.read() method.
    """
    text = values['fld_clipboard_content']

    transform_settings = get_transform_settings(values)
    text_transformer = TextTransformer(transform_settings)

    transformation_success = False
    try:
        transform_result = text_transformer.transform(text)
        transformation_success = True
    except TextTransformerError as e:
        errmsg = """ Please check your surrounding text. It seems to be invalid.\
        A valid surrounding text must only contain the format code {{}} or {{0}}.\
        
        
        Error message: {0}
        """.format(str(e)).strip()
        sg.popup_error(errmsg, title="Text transformation error")

    if transformation_success:
        print(transform_result)
        window['fld_preview'].update(transform_result['transformed_text'])
        txt_count_lines = "Preview contains {0} text items(s)".format(transform_result['count_text_items'])
        window['txt_prv_count_lines'].update(txt_count_lines)

        if transform_result['transformed_text'] == '':
            window['btn_copy_to_clipboard'].update(disabled=True)
        else:
            window['btn_copy_to_clipboard'].update(disabled=False)


def clicked_copy_to_clipboard(values):
    """
    Lets the user copy the preview of the transformed text to the clipboard.

    Args:
        values (dict): The values dictionary returned by the windows.read() method.
    """
    pyperclip.copy(values['fld_preview'])


def typed_clipboard_content(window, values):
    """
    Reacts on the user typing in the text input field of the "Text input" frame.
    Currently, it only updates the label showing the count of lines of the input text.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        values (dict): The values dictionary returned by the windows.read() method.
    """
    text = values['fld_clipboard_content']
    update_count_lines(window, text)


def show_dialog_add_preset():
    """
    Displays a modal dialog which lets the user create and save a new preset.

    Returns:
        A new instance of a TransformSettingsPreset object if the user clicked the "Save" button.
        If the user cancels the dialog, None is returned.
    """
    fl_preset_options = [
        [sg.Text('Name', size=(9, 1)), sg.InputText(default_text='', key='preset_name')],
        [sg.Text('Prefix', size=(9, 1)),
         sg.InputText(default_text='',
                      key='prefix',
                      size=(5, 1)),
         sg.Checkbox('Line up', default=False, key='chk_line_up')],
        [sg.Text('Suffix', size=(9, 1)),
         sg.InputText(default_text='',
                      key='suffix', size=(5, 1)),
         sg.Checkbox('Quote text',
                     default=False,
                     key='chk_quote_text',
                     enable_events=True)],
        [sg.Text('Delimiter', size=(9, 1)),
         sg.InputText(default_text='',
                      key='delimiter', size=(5, 1)),
         sg.Text('Quote char'), sg.InputText(default_text='',
                                             size=(5, 1),
                                             key='fld_quote_char',
                                             disabled=True),
         sg.Text('Escape char'), sg.InputText(default_text='',
                                              size=(5, 1),
                                              key='fld_escape_char',
                                              disabled=True)
         ],
        [sg.Text('Surrounding text')],
        [sg.Multiline('', size=(55, 3), key='fld_surrounding_text')]
    ]

    layout = [
        [sg.Frame('New preset', fl_preset_options)],
        [sg.Button('Save', key='btn_save_preset'),
         sg.Button('Cancel', key='btn_cancel_preset')]
    ]
    window = sg.Window("Add new preset", layout, use_default_focus=True, finalize=True, modal=True)

    tsp = None

    while True:
        event, values = window.read()
        if event == 'chk_quote_text':
            clicked_quote_text_checkbox(values, window)
        elif event == 'btn_save_preset':
            if not values['preset_name']:
                sg.popup_ok("Please provide a preset name.")
                continue
            transform_settings = get_transform_settings(values)
            name = values['preset_name']
            tsp = TransformSettingsPreset(name, transform_settings)
            break
        else:
            break

    window.close()

    return tsp


def save_preferences(window, prefs):
    """
    Saves the current user preferences to a JSON file.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        prefs (:obj:`VicoPreferences`): The preferences object to be used.
    """
    presets = window['lbx_presets'].get_list_values()
    selected_preset_idx = window['lbx_presets'].get_indexes()[0]
    prefs.presets = presets
    prefs.selected_preset_index = selected_preset_idx
    prefs.save()


def update_preset_listbox(window, items, selected_index):
    """
    Updates the preset listbox with a new list of values and to highlight the selected preset.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        items: A new list of items to be displayed.
        selected_index (int): The selection index to be set.
    """
    window['lbx_presets'].update(items)
    window['lbx_presets'].update(set_to_index=selected_index)
    window['lbx_presets'].update(scroll_to_index=selected_index)


def update_displayed_preset(window, chosen_tsp):
    """
    Updates the displayed transform settings according to the given preset.

    Args:
        window (:obj:`PySimpleGUI.Window`): The window where the action should be performed.
        chosen_tsp (:obj:`TransformSettingsPreset`): The preset to be represented.
    """
    window['prefix'].update(chosen_tsp.transform_settings.prefix)
    window['suffix'].update(chosen_tsp.transform_settings.suffix)
    window['delimiter'].update(chosen_tsp.transform_settings.delimiter)
    window['chk_line_up'].update(chosen_tsp.transform_settings.line_up)
    window['chk_quote_text'].update(chosen_tsp.transform_settings.quote_text)
    window['fld_quote_char'].update(chosen_tsp.transform_settings.quote_char)
    window['fld_escape_char'].update(chosen_tsp.transform_settings.escape_char)
    window['fld_surrounding_text'].update(chosen_tsp.transform_settings.surrounding_text or '')

    values = {'chk_quote_text': chosen_tsp.transform_settings.quote_text}
    clicked_quote_text_checkbox(values, window)


def get_transform_settings(values):
    """
    Returns the currently displayed transform settings.

    Args:
        values (dict): The values dictionary returned by the windows.read() method.

    Returns:
        A new instance of a TransFormSettings object.
    """
    prefix, suffix, delimiter = values['prefix'], values['suffix'], values['delimiter']
    line_up = values['chk_line_up']
    quote_text = values['chk_quote_text']
    quote_char = values['fld_quote_char']
    escape_char = values['fld_escape_char']
    surrounding_text = values['fld_surrounding_text']
    transform_settings = TransformSettings(prefix=prefix, suffix=suffix, delimiter=delimiter, line_up=line_up,
                                           quote_text=quote_text, quote_char=quote_char,
                                           escape_char=escape_char, surrounding_text=surrounding_text)
    return transform_settings


def get_count_text_lines(text):
    """
    Returns the count of lines in a given text.
    If the given input is None or not of type str the value 0 is returned.

    Args:
        text (str): The text where the count of lines should be calculated.

    Returns:
        The count of lines in the given text as a number.
    """
    if not text:
        return 0

    if type(text) is not str:
        return 0

    count_text_lines = len(text.strip().splitlines())
    return count_text_lines
