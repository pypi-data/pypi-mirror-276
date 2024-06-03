##################################################
# Imports
##################################################
import decimal
# https://packaging.python.org/en/latest/tutorials/packaging-projects/

##################################################
# Significant Figures Implementation
##################################################
class ManageFigures(object):

    def calculate_number_of_significant_figures(self, figure: int | float) -> int:
        """
        Significant figures are the digits of a number that are meaningful in terms of accuracy or precision.

        This function is designed to take a number, it can either be a integer or a float, 
        and return the number of significant figures, following the significant figures rules.
        Non-zero digits are always significant, zeros between non-zero digits are always significant (9009)

        Args:
            figure (int | float): The number that we want to calculate

        Usage:
            >>> from <module> import calculate_number_of_significant_figures
            >>> calculate_number_of_significant_figures(344.50)
            >>> 5
            
        Returns:
            int: Representing the number of significant figures
        """
        ##############################
        # Significant Figures Rules
        ##############################
        # - non zero digits are Always significant
        # - zeros in between non-zero digits are always significant 
        # example: 80989
        # - leading zeros are never significant
        # 0,0009 ===> 1 significant figure
        # - trailing zeros are only significant if the number contains a decimal point

        # 3450 ===> 3 significant figures
        # 8009 ===> 4 significant figures
        # 32243 ===> 5 significant figures

        trailing_number_of_zeros = 0
        leading_number_of_zeros = 0

        if isinstance(figure, int):
            number_of_significant_figures = list(str(figure))

            if '0' not in number_of_significant_figures:
                return len(number_of_significant_figures)

            elif number_of_significant_figures[-1] == '0':
                for number in number_of_significant_figures[::-1]:
                    if number == '0':
                        trailing_number_of_zeros += 1
                    else:
                        break
                return len(number_of_significant_figures) - trailing_number_of_zeros
            else:
                return len(number_of_significant_figures)
        
        elif isinstance(figure, float):
            number_of_significant_figures = list(format(figure, 'f'))
            
            if '.' in number_of_significant_figures[1] and number_of_significant_figures[0] == '0':
                for number in number_of_significant_figures:
                    if number == '0':
                        leading_number_of_zeros += 1
                    elif number == '.':
                        continue
                    else:
                        break
            elif number_of_significant_figures[0] != '0':
                return len(number_of_significant_figures) - 1
            
            return ((len(number_of_significant_figures) - 1) - leading_number_of_zeros)
                        
                
                # if last number is zero
                # count the number of zeros starting from the last zero
                # get the total number of zeros and subtract it from the len of the original array



    # print(calculate_number_of_significant_figures(340500))
    # print(calculate_number_of_significant_figures(102030))
    # print(calculate_number_of_significant_figures(4050600))
    # print(calculate_number_of_significant_figures(700800900))
    # print(calculate_number_of_significant_figures(1002003000))
    # print(calculate_number_of_significant_figures(120030040))
    # print(calculate_number_of_significant_figures(500060007000))
    # print(calculate_number_of_significant_figures(18009000))
    # print(calculate_number_of_significant_figures(900040000))
    # print(calculate_number_of_significant_figures(306050))
    # print(calculate_number_of_significant_figures(40005000600))

    # https://packaging.python.org/en/latest/tutorials/packaging-projects/

    # def convert_integer_to_scientific_notation(self, figure: int) -> float:
    #     """
    #     description

    #     Args:

    #     Returns:
    #         float: the integer converted to a floating point value
    #     """
    #     to_list = list(str(figure))
    #     to_list.insert(1, '.')
    #     number_of_significant_figures = ManageFigures.calculate_number_of_significant_figures(to_list)

        



    # def convert_scientific_notation_to_integer(self):
    #     pass