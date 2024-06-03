##################################################
# Imports
##################################################
from math import pi


##################################################
# Formulas Class Implementation
##################################################
class GeneralFormulas(object):

    def calculate_volume_of_a_cylinder(self, height: int | float, radius: int | float) -> int | float:
        """
        This function is used to calcute the volume of a cylinder

        Args:
            height: the specified height of the cylinder
            raidus: the radius of the cylinder 

        Returns:
            the result of applying the calculations
        """
        arr = []
        
        arr.append(len(str(height)))
        arr.append(len(str(radius)))

        arr.sort()

        return round(height*pi*(pow(radius, 2)), arr[0])
    
    
    def calculate_volume_of_a_sphere(self, radius: int | float) -> int | float:
        """
        This function is used to calculate the volume of a sphere

        Args:
            radius: the radius of the sphere

        Returns:
            the result of applying the formula

        """
        return (4*pi*(pow(radius, 3))) / 3