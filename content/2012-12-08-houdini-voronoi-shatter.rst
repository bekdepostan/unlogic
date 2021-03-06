Houdini voronoi shatter
#######################

:title: Houdini voronoi shatter
:date: 2012-12-08T00
:tags:


Thought I would write about creating a very simple voronoi shatter effect in Houdini and how to explode it. The video below demonstrates the effect we're looking to achieve:

.. raw:: html

    <iframe src="https://player.vimeo.com/video/55168444" width="500" height="375" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
    <p><a href="https://vimeo.com/55168444">voronoi</a> from <a href="https://vimeo.com/user1380774">Sven</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

The process of creating this is very simple, and I learned a few things from setting this up, so I figured I would share and hope you learn something from it too.

So first we need to drop down a :code:`Geometry` node and dive inside. Delete the file node and then create a :code:`box` node. This box will be the object we will shatter. But in order to create a voronoi shatter we also need some seed points to generate the pattern with. So let's do that first. We'll use our box to generate the points we need, so drop down a :code:`Points From Volume` node and connect the box to its input. Adjust the settings to your liking, or copy the ones below. I kept the number of points low as I wanted fewer and larger pieces.

.. image:: /images/points_from_vol.png


Now that we have our points we can drop down a :code:`Voronoi Fracture` node and connect the points to its second input. The only setting I changed was to turn on :code:`Connect Inside Edges`. Finally we need to connect the *box* node to the *Voronoi Shatter's* first input. Now make the *Voronoi shatter* visible and you should see your fractured geo.

.. image:: /images/fracture.png


Next we'll turn on the dynamics via the rigid bodies shelf at the top. Click *RBD Fracture* and make sure the voronoi geo is selected and press enter. If you press play now your object will fall down. Hrmmm, not totally awesome, as we wanted to explode it a little too. So the plan is to make all the pieces explode from the outwards, like, for example, along the normals of a sphere say? Yes, that sounds about right. Ok, so let's put down a *Sphere* and scale it so that it's roughly the same size as the box. Append a *Point* node to the sphere and add a *Normal* and *Velocity* attribute. The *Velocity* attribute is under the *Particle* tab and we'll set its value to be a facture of the point's normal. Feel free to play with this value to get the efect you want. Basically this will set the point's velocity to the normal at that point, causing the pieces to rediate outwards when the sim starts.

.. image:: /images/vel_attribute.png


Connect the output to the second input of an *Attribute Transfer* node and then connect the output of that to the *Rest Position* node. Connect the *Box* to the first input of the *Attribute Transfer* node. This will transfer the point attributes of the *Sphere* onto the shattered geo. You should now have a network that looks like this:

.. image:: /images/finalnetwork.png


And yet still to exploding pieces? Well, we need to tell our solver to use the point velocity. So dive into the *Autodop Network* and on the *RBD Fracture Object* enable *Inherit Velocity From Point Velocity*. Hit play and you should see it explode.

.. image:: /images/inherit_pv.png

