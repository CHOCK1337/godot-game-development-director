import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
SPEC=importlib.util.spec_from_file_location('va',ROOT/'scripts/validate_accessibility_localization.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
class Tests(unittest.TestCase):
    def test_requires_core_options(self):
        d={"locales":["zh_CN","en"],"subtitles":{"enabled":True,"speaker_labels":True},"input_remap":True,"reduced_motion":True,"text_expansion_test":1.35,"screen_reader_labels":True}
        self.assertEqual(MOD.validate(d),[])
    def test_missing(self):
        d={"locales":["zh_CN"],"subtitles":{"enabled":False},"input_remap":False,"reduced_motion":False,"text_expansion_test":1.0,"screen_reader_labels":False}
        self.assertGreaterEqual(len(MOD.validate(d)),4)
if __name__=='__main__': unittest.main()
