Bounding box of rotated image
#############################

:title: Bounding box of rotated image
:date: 2009-12-04T17
:tags: 


In a previous post I mentioned about finding the width and height of the bounding box of a rotated rectangle, in this post I will explain the math in more detail. Given a 2D rectangle and an arbitrary angle of rotation, how do we work out the new bounding box of the rectangle?

<!--more-->

I'll use the image below to help illustrate:

.. image:: "/images/content/bbox.jpg"


The blue rectangle is our original shape and the red one our (obviously) newly rotated rectangle. α is the angle we’ve rotated by in degrees Let’s think back to maths class and try to remember our trigonometry. In order to find the length of a given side in a right angled triangle we take one of the known sides and an angle and apply sin, cos or tan accordingly.

Our aim here is to find h1, h2, w1, and w2 in order to get

    h' = h1 + h2
    w' = w1 + w2

Where h’ and w’ are the new width and height of the bounding box. Let’s start with w1 and h1, referring back to the top right triangle in the diagram. We know the length of the hypotenuse so we need to use cos for w1 (adjacent) and then for h1 (opposite) we need to use sin

    w1 = h * sin(a) 
    h1 = h * cos(a)

Half way there. Next we find w2 and h2 in a similar way

    w2 = w * cos(a)
    h2 = w * sin(a)

Now all we need to do is add h1 and h2 together to get h’ and w1 to w1 to get w’. In code that is

.. code:: c

	    float h_dash = h*fabs(cos(alpha)) + w*fabs(sin(alpha));
	    float w_dash = w*fabs(cos(alpha)) + h*fabs(sin(alpha));

The more astute of you may have noticed that this is slightly different to what I posted in my previous article. That’s because I noticed I can do away with beta and use just the angle of rotation. In terms of execution time this means very little as beta is obtained once by subtraction alpha from 90, but in a neatness sense it’s an improvement.
