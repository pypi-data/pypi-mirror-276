##################################################
# Imports
##################################################
from unittest import TestCase
from halting.formulas.formulas import GeneralFormulas

##################################################
# General Formulas TestCase Implementation
##################################################

class GeneralFormulasTestCase(TestCase):

    def test_volume_of_a_cyclinder_returns_expected_data(self):
        expected_result = 25.1
        general_formulas = GeneralFormulas()
        result = general_formulas.calculate_volume_of_a_cylinder(height=2, radius=2)
        
        self.assertEqual(expected_result, result)

    