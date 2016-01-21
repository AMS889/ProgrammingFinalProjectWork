from Visualization import *
from main_funcs import clean_input
import os
import unittest

'''

Author: Nora Barry

This module contains tests for the visualization class and an input cleaning function in main_funcs.py

'''

class Test1(unittest.TestCase):

    def test_visualization_class(self):
        #create instances of visualization class for various zipcodes
        visual_1 = visualization(10038, 12, 'Monday', 12)
        visual_2 = visualization(10001, 11, 'Tuesday', 1)
        visual_3 = visualization(10013, 10, 'Wednesday', 2)
        visual_4 = visualization(11201, 9, 'Thursday', 3)
        visual_5 = visualization(11101, 8, 'Friday', 4)
        
        self.assertIsInstance(visual_1, visualization)
        self.assertIsInstance(visual_2, visualization)
        self.assertIsInstance(visual_3, visualization)
        self.assertIsInstance(visual_4, visualization)
        self.assertIsInstance(visual_5, visualization)
        
    def test_basemap(self):
        #create two instances of the visualization class
        visual_1 = visualization(10038, 12, 'Monday', 12)
        visual_2 = visualization(10001, 11, 'Tuesday', 1)
        
        #call the basemapPlot function, which saves a copy of the plot if the user inputs 'Y'
        visual_1.basemapPlot('Y')
        visual_2.basemapPlot('N') 
        self.assertTrue(os.path.isfile("MapOfCitiBikeAvailabilityForMondaysInMonth12atHour12.pdf"))
        self.assertFalse(os.path.isfile("MapOfCitiBikeAvailabilityForTuesdaysInMonth11atHour1.pdf"))
                         
    def test_barplot(self):
        visual_3 = visualization(10013, 10, 'Wednesday', 2)
        visual_4 = visualization(11201, 9, 'Thursday', 3)
        
        visual_3.barPlot('Y')
        visual_4.barPlot('N')                
        self.assertTrue(os.path.isfile("PlotOfCitiBikesAvailableOnWednesdaysMonth10Hour2Zip10013.pdf"))
        self.assertFalse(os.path.isfile("PlotOfCitiBikesAvailableOnThursdaysInMonth9atHour3Zip11201.pdf"))
                         
    def test_input_clean(self):
        self.assertEqual(clean_input('      December'), 'december')
        self.assertEqual(clean_input('MONDAY   '), 'monday')
        self.assertEqual(clean_input('TUESDAY'), 'tuesday')
        
if __name__ == '__main__':
    unittest.main()                         
               