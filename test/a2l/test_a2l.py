from pathlib import Path
import unittest
from pya2ltools.a2l.reader.reader import read_a2l
from pya2ltools.a2l.writer.writer import write_a2l_file


class TestA2l(unittest.TestCase):
    def test_a2l(self):
        path = Path("test") / "ECU_Description" / "ASAP2_Demo_V171.a2l"
        output = Path("a2l_out.a2l")
        a2l_file = read_a2l(path)
        write_a2l_file(a2l_file, output)
        a2l_file_new = read_a2l(output)

        # for i, m in enumerate(a2l_file.project.modules[0].global_list):
        #     m_new = a2l_file_new.project.modules[0].global_list[i]
        #     self.assertEqual(m, m_new)

        for i, c in enumerate(a2l_file.project.modules[0].characteristics):
            c_new = a2l_file_new.project.modules[0].characteristics[i]
            self.assertEqual(c, c_new)
