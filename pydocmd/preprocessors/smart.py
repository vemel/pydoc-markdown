from pydocmd.preprocessors.rst import Preprocessor as RSTPreprocessor
from pydocmd.preprocessors.google import Preprocessor as GooglePreprocessor


class Preprocessor(object):
    """
    This class implements the preprocessor for restructured text and google.
    """
    def __init__(self, config=None):
        self.config = config
        self._google_preprocessor = GooglePreprocessor(config)
        self._rst_preprocessor = RSTPreprocessor(config)

    def is_google_format(self, docstring):
        """
        Check if `docstring` is written in Google docstring format

        https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
        """
        lines = [line.strip() for line in docstring.split('\n')]
        google_section_names = self._google_preprocessor.get_section_names()
        for section_name in google_section_names:
            if section_name in lines:
                return True

        return False

    def preprocess_section(self, section):
        """
        Preprocessors a given section into it's components.
        """
        
        if self.is_google_format(section.content):
            return self._google_preprocessor.preprocess_section(section)

        return self._rst_preprocessor.preprocess_section(section)

    @staticmethod
    def _append_section(lines, key, sections):
        section = sections.get(key)
        if not section:
            return

        if lines and lines[-1]:
            lines.append('')

        # add an extra line because of markdown syntax
        lines.extend(['**{}**:'.format(key), ''])
        lines.extend(section)
