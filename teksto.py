import os
import uuid


class TextTransformerError(Exception):
    """Raised when a text transformation fails.

    Args:
        message (str): Human readable string describing the exception.

    Attributes:
        message (str): Human readable string describing the exception.
    """
    def __init__(self, message):
        self.message = message


class TransformSettingsPreset(object):
    """
    Keeps together an instance of a TransformSettings object and a name.

    Has a factory method from_dict() to create an instance from a dictionary
    This method is used while loading the user preferences.
    The method to_dict() returns a representation of the instance as a dictionary.
    This method is used while saving the user preferences.

    Attributes:
        name (str): Name of the preset.
        identifier (UUID): Unique id of the preset.
        transform_settings (:obj:`TransformSettings`): The transform settings of the preset.
    """
    @staticmethod
    def from_dict(dict_rep):
        """
        Returns a new instance of a TransformSettingsPreset object created from a dictionary.

        Args:
            dict_rep (dict): A dictionary containing the representation of a TransformSettingsPreset object.
                See also the instance method to_dict().

        Returns:
            An instance of a TransformSettingsPreset object.
        """
        name = dict_rep['name']
        ts_dict = dict_rep['transform_settings']
        transform_settings = TransformSettings(prefix=ts_dict.get('prefix', ''),
                                               suffix=ts_dict.get('suffix', ''),
                                               delimiter=ts_dict.get('delimiter', ''),
                                               line_up=ts_dict.get('line_up', False),
                                               quote_text=ts_dict.get('quote_text', False),
                                               quote_char=ts_dict.get('quote_char', None),
                                               escape_char=ts_dict.get('escape_char', None),
                                               surrounding_text=ts_dict.get('surrounding_text', None))
        tsp = TransformSettingsPreset(name, transform_settings)
        return tsp

    def __init__(self, name, transform_settings):
        """
        Initializes a new instance of a TransformSettingsPreset object.

        Args:
            name (str): Name of the preset.
            transform_settings (:obj:`TransformSettings`): The transform settings of the preset.
        """
        self._name = name
        self._identifier = uuid.uuid1()
        self._transform_settings = transform_settings

    def to_dict(self):
        """
        Returns a representation of the current instance as a dictionary.
        See also the static method from_dict().

        Returns:
            A dictionary representing the current instance.
        """
        dict_rep = {
                        'name': self._name,
                        'transform_settings': {
                                                    'prefix': self._transform_settings.prefix,
                                                    'suffix': self._transform_settings.suffix,
                                                    'delimiter': self._transform_settings.delimiter,
                                                    'line_up': self._transform_settings.line_up,
                                                    'quote_text': self._transform_settings.quote_text,
                                                    'quote_char': self._transform_settings.quote_char,
                                                    'escape_char': self._transform_settings.escape_char,
                                                    'surrounding_text': self._transform_settings.surrounding_text
                                              }
                   }
        return dict_rep

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def identifier(self):
        return self._identifier

    @property
    def transform_settings(self):
        return self._transform_settings

    @transform_settings.setter
    def transform_settings(self, transform_settings):
        self._transform_settings = transform_settings

    def __repr__(self):
        return self._name


class TransformSettings(object):
    """
    Holds a set of options that are needed to control the text transformation executed
    by a TextTransformer object.

    Attributes:
        prefix (str): The prefix to be placed before the text item.
        suffix (str): The suffix to be placed after the text item.
        delimiter (str): The delimiter to be placed between the text items.
        line_up (bool): Should the text items be lined up one after another on one line?
        quote_text (bool): Should the text containing the text items be quoted?
        quote_char (str): The character to be quoted.
        escape_char (str): The escape character to be used to quote quote_char.
        surrounding_text (str): The surrounding text where the transformed text should be placed in.
    """
    def __init__(self, prefix, suffix, delimiter, line_up=False,
                 quote_text=False, quote_char=None, escape_char=None, surrounding_text=None):
        """
        Initializes a new instance of a TransformSettings object.

        Args:
            prefix (str): The prefix to be placed before the text item. Default is ''.
            suffix (str): The suffix to be placed after the text item. Default is ''.
            delimiter (str): The delimiter to be placed between the text items. Default is ''.
            line_up (bool): Should the text items be lined up one after another on one line? Default is False.
            quote_text (bool): Should the text containing the text items be quoted? Default is False.
            quote_char (str): The character to be quoted. Default is None
            escape_char (str): The escape character to be used to quote quote_char. Default is None.
            surrounding_text (str): The surrounding text where the transformed text should be placed in.
                Default is None.
        """
        self._prefix = prefix or ''
        self._suffix = suffix or ''
        self._delimiter = delimiter or ''
        self._line_up = line_up
        self._quote_text = quote_text
        self._quote_char = quote_char
        self._escape_char = escape_char
        self._surrounding_text = surrounding_text

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix or ''

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        self._suffix = suffix or ''

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, delimiter):
        self._delimiter = delimiter or ''

    @property
    def line_up(self):
        return self._line_up

    @line_up.setter
    def line_up(self, line_up):
        self._line_up = line_up

    @property
    def quote_text(self):
        return self._quote_text

    @quote_text.setter
    def quote_text(self, quote_text):
        self._quote_text = quote_text

    @property
    def quote_char(self):
        return self._quote_char

    @quote_char.setter
    def quote_char(self, quote_char):
        self._quote_char = quote_char

    @property
    def escape_char(self):
        return self._escape_char

    @escape_char.setter
    def escape_char(self, escape_char):
        self._escape_char = escape_char

    @property
    def surrounding_text(self):
        return self._surrounding_text

    @surrounding_text.setter
    def surrounding_text(self, surrounding_text):
        self._surrounding_text = surrounding_text


class TextTransformer(object):
    """
    Performs the transformation of a text using the specified transform settings.
    """

    def __init__(self, transform_settings):
        """
         Initializes a new instance of a TransformSettings object.

         Args:
             transform_settings (:obj:`TransformSettings`): The transform settings to be used
                    for the text transformation.
        """
        self._transform_settings = transform_settings

    def transform(self, text):
        """
        Transforms the given text using the transform settings specified during initialization.

        Args:
            text (str): The text to be transformed.

        Returns:
            A dictionary containing the transformed text (key: 'transformed_text')
            and the count of text items (key: 'count_text_items').

        Raises:
            TypeError: If text is not of type str.
        """
        if not text:
            dict = {'transformed_text': text, 'count_text_items': 0}
            return dict

        if type(text) is not str:
            msg = "Given value is not of type str, but of type {0}".format(type(text))
            raise TypeError(msg)

        if self._transform_settings.quote_text:
            text = self._quote_text(text)

        lines = text.splitlines()
        # removing empty lines
        lines = [line for line in lines if len(line.strip()) > 0]
        # stripping whitespace from the line
        lines = [line.strip() for line in lines]
        lines = self._place_prefix(lines)
        lines = self._place_suffix(lines)
        lines = self._place_delimiter(lines)
        count_text_items = len(lines)
        transformed_text = self._concatenate(lines)
        transformed_text = self._surroundwithtext(transformed_text)

        dict = {'transformed_text': transformed_text, 'count_text_items': count_text_items}
        return dict

    def _quote_text(self, text):
        """
        Quotes the given text according to the transform settings specified during initialization.

        Args:
            text (str): The text to be quoted.

        Returns:
            The quoted text.
        """
        escape_char = self._transform_settings.escape_char + self._transform_settings.quote_char
        quoted_text = text.replace(self._transform_settings.quote_char, escape_char)
        return quoted_text

    def _place_prefix(self, lines):
        """
        Places the prefix specified in the transform settings before every line.

        Args:
            lines (:obj:`list` of :obj:`str`): The lines to be processed.

        Returns:
            The transformed lines.
        """
        transformed_lines = []
        for line in lines:
            transformed_line = "{0}{1}".format(self._transform_settings.prefix, line)
            transformed_lines.append(transformed_line)
        return transformed_lines

    def _place_suffix(self, lines):
        """
        Places the suffix specified in the transform settings after every line.

        Args:
            lines (:obj:`list` of :obj:`str`): The lines to be processed.

        Returns:
            The transformed lines.
        """
        transformed_lines = []
        for line in lines:
            transformed_line = "{0}{1}".format(line, self._transform_settings.suffix)
            transformed_lines.append(transformed_line)
        return transformed_lines

    def _place_delimiter(self, lines):
        """
        Places the delimiter specified in the transform settings between the lines.

        Examples:
            delimiter = ","
            ['foo'] => ['foo']
            ['foo', 'bar'] => ['foo,', 'bar']
            ['foo', 'moo', 'bar'] => ['foo,', 'moo,' 'bar']

        Args:
            lines (:obj:`list` of :obj:`str`): The lines to be processed.

        Returns:
            The transformed lines.
        """
        if len(lines) in [0, 1]:
            return lines
        transformed_lines = []
        for i in range(0, len(lines) - 1):
            line = lines[i]
            transformed_line = "{0}{1}".format(line, self._transform_settings.delimiter)
            transformed_lines.append(transformed_line)
        transformed_lines.append(lines[-1])

        return transformed_lines

    def _concatenate(self, lines):
        """
        Concatenates the lines according to the transform settings specified during initialization.

        Args:
            lines (:obj:`list` of :obj:`str`): The lines to be processed.

        Returns:
            The final version of the transformed text.
        """
        if not self._transform_settings.line_up:
            newline_char = os.linesep
        else:
            newline_char = ' '

        transformed_text = newline_char.join(lines)
        return transformed_text

    def _surroundwithtext(self, transformed_text):
        """
        Places the transformed into the surrounding text in case it was specified during initialization.

        Args:
            transformed_text (str): The already transformed text.

        Returns:
            If no surrounding text was specified during initialization the transformed text is returned.
            Otherwise the combination of the transformed text within the surrounding text is returned.

        Raises:
            TextTransformerError if formatting the text throws an exception.
        """
        if self._transform_settings.surrounding_text:
            try:
                transformed_text = self._transform_settings.surrounding_text.format(transformed_text)
            except IndexError as e:
                errmsg = "The format of the surrounding text seems to be broken: {0}".format(str(e))
                raise TextTransformerError(errmsg)

        return transformed_text
