# a sample utility function to validate the radius of a sphere for non-negativity.
# This function can be used to validate user input or input from other sources to ensure that the radius is a valid value. 
def validate_radius(radius):
    """
    Validate that the radius is a non-negative number.

    Parameters:
    radius (float): The radius of the sphere.

    Returns:
    bool: True if the radius is valid, else False.
    """

    return radius >= 0
