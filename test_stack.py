import unittest
import copy

import docutils
import docutils.examples
import yaml

import stack


class TestStack(unittest.TestCase):

    def test_cleanup(self):
        obj = {
            '__': 'overwrite',
            'l': [{'__': 'merge-last'}]
            }
        self.assertEqual(stack._cleanup(obj), {'l': []})

    def test_merge(self):
        # parse the readme and check that the merging scenarios are corrects
        with open('README.rst', 'r') as f:
            doc, pub = docutils.examples.internals(
                f.read(), input_encoding='utf8')
            for table in doc.traverse(condition=docutils.nodes.table):
                for row in table.traverse(condition=docutils.nodes.row)[1:]:
                    if len(row) != 3: continue
                    before, data, after = (yaml.load(c.astext()) for c in row)
                    merged = stack._merge_dict(
                        copy.deepcopy(before), copy.deepcopy(data))
                    before_yml, data_yml, after_yml, merged_yml = (
                        yaml.dump(yml, default_flow_style=False) for yml in (
                            before, data, after, merged))
                    self.assertEqual(
                        merged, after, msg='\n'.join([
                            '\nBEFORE =>', before_yml,
                            'DATA =>', data_yml,
                            'MERGES TO =>', merged_yml,
                            'INSTEAD OF =>', after_yml,
                            ]))


if __name__ == '__main__':
    unittest.main()
