import unittest
import unittest.mock as um

from unittest.mock import patch, MagicMock

from test_module.FileOpener import FileRead

builtin_open = open

"""
https://gist.github.com/adammartinez271828/137ae25d0b817da2509c1a96ba37fc56#gistcomment-3584241
"""
def mapped_mock_open(file_contents_dict):
    """Create a mock "open" that will mock open multiple files based on name
    Args:
        file_contents_dict: A dict of 'fname': 'content'
    Returns:
        A Mock opener that will return the supplied content if name is in
        file_contents_dict, otherwise the builtin open
    """
    mock_files = {}
    for fname, content in file_contents_dict.items():
        mock_files[fname] = um.mock_open(read_data=content).return_value

    def my_open(fname, *args, **kwargs):
        if fname in mock_files:
            return mock_files[fname]
        else:
            return builtin_open(fname, *args, **kwargs)

    mock_opener = um.Mock()
    mock_opener.side_effect = my_open
    return mock_opener


class MyTestCase(unittest.TestCase):

    def test_FileOpen(self):
        with um.patch('builtins.open', um.mock_open(read_data='testing read file')):
            FileRead(file_path='/opt/some/path/to/file').open_and_read()            
            
    @patch('builtins.open', new_callable=um.mock_open, read_data="test read file 2")
    def test_FileOpen_2(self, mo):
        FileRead(file_path='/opt/some/path/to/file').open_and_read()

    @patch('builtins.open', new_callable=um.mock_open, read_data="test read file multi file")
    def test_FileOpen_multi(self, mo):
        handlers = (mo.return_value, um.mock_open(read_data="somefile read").return_value,)
        mo.side_effect = handlers
        FileRead(file_path='/opt/some/path/to/file').open_and_read()

    @patch('builtins.open', new=mapped_mock_open({
        '/opt/some/path/to/file': 'C file content',
        '/opt/some/path/to/some_file.txt': 'B file content',
    }))
    def test_FileOpen_multi_specific(self):
        FileRead(file_path='/opt/some/path/to/file').open_and_read()

    def test_FileOpen_multi_specific_2(self):
        with patch('builtins.open', new=mapped_mock_open({
            '/opt/some/path/to/file': 'C file content',
            '/opt/some/path/to/some_file.txt': 'B file content',
            }))  as mapped_mo:
            FileRead(file_path='/opt/some/path/to/file').open_and_read()

        mapped_mo.assert_any_call('/opt/some/path/to/file', 'r')
        mapped_mo.assert_any_call('/opt/some/path/to/some_file.txt')

            
if __name__ == '__main__':
    unittest.main()
