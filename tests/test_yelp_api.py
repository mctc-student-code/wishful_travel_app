import unittest
from unittest import TestCase
from unittest.mock import patch
from API import yelp_api


class YelpapiTest(unittest.TestCase):

    def setUp(self):
        self.a = 'state'
        self.b = 'city'
 
    def test_get_location(self): #Testing  get restaurants() in retrieving location    
        #Arrange
        print("Test 1: ")
        #Action
        result = yelp_api.get_restaurants_for_location('Minneapolis, MN')
        #Assert
        print(result)
        self.assertIsNotNone(result, None)
    
    """Checking yelp api for no locations"""
    
    @patch('requests.Response.json',return_value= {'error': {'code': 'LOCATION_NOT_FOUND', 'description':'Could not execute search, try specifying a more exact location.'}})
     
    def test_get_no_restaurants_for_location(self, mock_get_restaurants_for_location):
        n_location = yelp_api.get_restaurants_for_location('My location123')
        print(n_location)
             
    if __name__ == "__main__":
     unittest.main()            

        



           