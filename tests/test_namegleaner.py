# -*- coding: utf-8 -*-

from nose.tools import assert_equal
from batchplotlib4.namegleaner import NameGleaner

class TestInit:
    def test_one_at_a_time(self):
        """Categories can be added one at a time"""
        ng = NameGleaner()
        ng.add_category('current', r'(\d+)uA')
        ng.add_category('bfield', r'(\d+)G')
        assert_equal(sorted(ng.categories.keys()), ['bfield', 'current']) 

    def test_all_at_once_as_kwargs(self):
        '''Categories can be added all at once'''
        ng = NameGleaner(current=r'(\d+)uA', bfield=r'(\d+)G')
        assert_equal(sorted(ng.categories.keys()), ['bfield', 'current']) 

class TestGlean:
    @classmethod
    def setup(cls):
        cls.fname1 = (r"F:\Rzchlab\Google Drive\BiFe\B737_1\amr_vs_angle"
                r"\141119\300uA_20G_-170to170deg_poldown\data_table.txt")
        cls.fname2 = (r"F:\Rzchlab\Google Drive\BiFe\B737_1\amr_vs_angle"
                r"\141119\20G_-170to170deg_poldown\data_table.txt")
        cls.ng = NameGleaner(current     = '(\d+)uA',
                             bfield      = '(\d+)G',
                             start_angle = '(-?\d+)to',
                             end_angle   = '(-?\d+)deg',
                             pol         = 'pol(up|down)')

    def test_glean_without_categories(self):
        empty_ng = NameGleaner()
        d = empty_ng.glean(self.fname1)
        assert_equal(d, {})

    def test_glean(self):
        d = self.ng.glean(self.fname1)
        correct = {'current' : '300', 'bfield' : '20', 'start_angle' : '-170',
                   'end_angle' : '170', 'pol' : 'down'}
        assert_equal(d, correct)

    def test_glean_missing_category(self):
        d = self.ng.glean(self.fname2, fill_obj='x')
        correct = {'current' : 'x', 'bfield' : '20', 'start_angle' : '-170',
                   'end_angle' : '170', 'pol' : 'down'}
        assert_equal(d, correct)

    def test_should_translate(self):
        self.ng.translate(category='current', value='300', translation='0.3')
        d = self.ng.glean(self.fname1)
        assert_equal(d['current'], '0.3')

    def test_shouldnt_translate(self):
        self.ng.translate(category='current', value='400', translation='0.4')
        d = self.ng.glean(self.fname1)
        assert_equal(d['current'], '300')

    def test_translate_with_pattern(self):
        self.ng.regex_sub('current', pattern='.*', repl='butts')
        d = self.ng.glean(self.fname1)
        assert_equal(d['current'], 'butts')

    def test_translate_with_backref_pattern(self):
        self.ng.regex_sub('pol', pattern=r'.*(wn)', repl=r'p\1d')
        d = self.ng.glean(self.fname1)
        assert_equal(d['pol'], 'pwnd')

    def test_regex_sub_run_after_translate(self):
        self.ng.translate(category='current', value='300', translation='0.3')
        self.ng.regex_sub('current', r'(0)\.(3)', r'\1..\2')
        d = self.ng.glean(self.fname1)
        assert_equal(d['current'], '0..3')
