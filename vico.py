import PySimpleGUI as sg
from preferences import VicoPreferences
import ui

WINDOW_TITLE = 'vico'
DEBUG_MODE = True


def main():
    prefs = VicoPreferences()
    window = ui.prepare_main_window(WINDOW_TITLE, prefs)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if DEBUG_MODE:
            print(event, values)

        # If the main window closes we need to save the preferences
        if event in (sg.WIN_CLOSED, sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            ui.save_preferences(window, prefs)
            break

        # User clicked the "Copy from clipboard" button
        if event == 'btn_copy_from_clipboard':
            ui.clicked_copy_from_clipboard(window)

        # User clicked the "Clear" button below the text input
        if event == 'btn_clear_text_input':
            ui.clicked_clear_text_input(window)

        # User clicked the "Quote text" checkbox
        if event == 'chk_quote_text':
            ui.clicked_quote_text_checkbox(values, window)

        # User clicked on an item in the listbox displaying the presets,
        # so we need to update the display transform settings accordingly
        if event == 'lbx_presets':
            ui.clicked_preset_item(window, values)

        # User clicked the "Add" button to add a new preset
        if event == 'btn_add_preset':
            ui.clicked_add_preset(window)

        # User clicked the "Save" button to save the current
        # transform settings of the selected preset
        if event == 'btn_save_preset':
            ui.clicked_save_preset(window, values)

        # User clicked the "Delete" button to delete the selected preset
        if event == 'btn_del_preset':
            ui.clicked_delete_preset(window)

        # User clicked the "Move up" button to move the selected preset up
        if event == 'btn_move_preset_up':
            ui.move_selected_preset(window, ui.MOVE_DIRECTION_UP)

        # User clicked the "Move down" button to move the selected preset down
        if event == 'btn_move_preset_down':
            ui.move_selected_preset(window, ui.MOVE_DIRECTION_DOWN)

        # User clicked the "Preview" button to preview the text transformation
        if event == 'btn_preview':
            ui.clicked_show_preview(window, values)

        # User clicked on the "Copy to clipboard" button
        if event == 'btn_copy_to_clipboard':
            ui.clicked_copy_to_clipboard(values)

    window.close()


if __name__ == '__main__':
    main()
