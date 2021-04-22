"""
Polynomial regression
=====================
"""

###############################
# One way to visualize the evolution of a given epidemistic criterion
# as weel as its trend, is to use **vizcovidfr's poly_fit** function,
# which displays the scatter plot of the evolution of the given variable
# in the given region with a polynomial regression. The
# polynomial degree is chosen by minimizing the mean squared error.
# Let's take a look at the situation in hospital care of our overseas
# friends, in Martinique.

from vizcovidfr.regression import regression
regression.poly_fit(2, 2)

###############################
# To go further
# -------------
# If you're interested in knowing more about the goodness-of-fit
# of the above model, you can try to use the **R2** function with the
# same parameters as before, which will give you the coefficient of
# determination of the model, written :math:`R^2`.
# In this example, it would be:

regression.R2(2, 2)
