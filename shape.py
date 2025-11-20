import numpy as np
import trimesh

class Shape:

    def __init__(self, form, size=1.0):
        self.form = form
        self.size = size

    def create_3D_mesh(self):
        s = self.size
        f = self.form

        if f == "circle":

            mesh = trimesh.creation.cylinder(radius=s, height=0, sections=50)   # make a cylinder with height = 0
        
        elif f == "square":
            
            verts = np.array([
                [-s, -s, 0], [s, -s, 0], [s, s, 0], [-s, s, 0]                  # Coordinates of the edges of the square
            ])
            faces = np.array([[0, 1, 2], [0, 2, 3]])                            # Triangle surface units
            mesh = trimesh.Trimesh(vertices=verts, faces=faces)                 # Creating the mesh
        
        elif f == "triangle":

            verts = np.array([
                [0, s, 0], [s, -s, 0], [-s, -s, 0]                              # Coordinates of the edges of the triangle
            ])
            faces = np.array([[0, 1, 2]])                       
            mesh = trimesh.Trimesh(vertices=verts, faces=faces)               
        
        elif f == "sphere":

            mesh = trimesh.creation.icosphere(radius=s, subdivisions=3)         # Creates sphere approximation mesh                                                        # By changing subdivision we can adjust the approximation (< 5)
        
        elif f == "cube":

            mesh = trimesh.creation.box(extents=[s, s, s])                          # Creates cube mesh
        
        elif f == "pyramid":
            
            verts = np.array([
                [-s, -s, 0], [s, -s, 0], [s, s, 0], [-s, s, 0], [0, 0, s]       # We have a base square and then an apex
            ])
            faces = np.array([
                [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 1, 2], [0, 2, 3]
            ])                            
            mesh = trimesh.Trimesh(vertices=verts, faces=faces)                 # Creating the mesh

        else:
            raise ValueError("3D mesh not supported for shape {self.form}")
        
        return mesh

def create_mesh(shape_name, formation_name, shape_size=1.0, spacing=0.5, f_size1=10, f_size2=10, f_size3=10, count=10, r_step=0.5, theta_step=25, height_step=0.5):
    """
    Creates a formation of shapes in a Trimesh.Scene.
    
    dimension: "2D" or "3D" 
    shape_name: e.g. "cuboid", "sphere", "pyramid"
    formation_name: e.g. "grid", "radial"
    shape_size: size of shapes
    spacing: space between shapes (used in grid)
    f_size1, f_size2, f_size3: grid/cuboid dimensions
    count: number of shapes in radial formation
    r_step: how much radius increases per step (spiral)
    theta_step: how much the angle increases per step (spiral)
    height_step: how much the height increases per step (spiral 3D)
    """

    scene = trimesh.Scene()                                                     # We use Scene for a collection of meshes(shapes)
                                               
    if formation_name == "grid":                                                # f_size1 is length, f_size2 is width, f_size3 is height
        
        unit = spacing + shape_size                     
        count_len = int(f_size1 / unit)                                         # How many shapes on one row        
        count_width = int(f_size2 / unit)                                              
        count_height = int(f_size3 / unit)

        if (count_len * unit - spacing <= f_size1):                             # Checks if we can place one more shape at the end 
            count_len += 1

        if (count_width * unit - spacing <= f_size2):                           
            count_width += 1

        if (count_height * unit - spacing <= f_size3):                          
            count_height += 1

        for u in range(count_width):
            for v in range(count_len):
                for w in range(count_height):

                    shape = Shape(shape_name, shape_size)                               # Create shape instance
                    shape_mesh = shape.create_3D_mesh()                             
                    shape_mesh.apply_translation([u * unit, v * unit, w * unit])        # Move shape to the correct position
                    scene.add_geometry(shape_mesh)                                      # Add the mesh to the formation                           
        
    elif formation_name == "radial":                                            # f_size1 is the diameter, while we ignore the f_size2
        
        radius = f_size1 / 2.0   
        angles = np.linspace(0, 2*np.pi, count, endpoint=False)                 # With endpoint=False, it excludes the final value, otherwise we double count

        x = radius * np.cos(angles)                                             # Computes cos of the whole list angles
        y = radius * np.sin(angles)                                             # Computes sin of the whole list angles

        for xi, yi in zip(x, y):                                                # zip(x, y) makes tuples out of elements from both lists with same position
            
            shape = Shape(shape_name, shape_size)
            mesh = shape.create_3D_mesh()
            mesh.apply_translation([xi, yi, 0])
            scene.add_geometry(mesh)


    elif formation_name == "spiral" :                      
        
        for i in range(count):

            cur_radius = r_step * i                                             # Increase the radius
            cur_theta = theta_step * i                                          # Increase the angle
            cur_height = height_step * i                                        # Increase the height

            x = cur_radius * np.cos(cur_theta)                                  
            y = cur_radius * np.sin(cur_theta)

            shape = Shape(shape_name, shape_size)
            mesh = shape.create_3D_mesh()
            mesh.apply_translation([x, y, cur_height])
            scene.add_geometry(mesh)     

    elif formation_name == "sphere":                                           
        """
        Arrange shapes evenly on the surface of a sphere using Fibonacci sphere algorithm
        """

        phi = np.pi * (3.0 - np.sqrt(5.0))                                      # Golden angle

        for i in range(count):
            y = 1 - (2.0 * i) / (count - 1)                                     # y goes from 1 to -1
            r = np.sqrt(1 - y * y)                                              # Radius at y
            theta = phi * i                                                     # Golden angle increment

            x = np.cos(theta) * r
            z = np.sin(theta) * r

            pos = np.array([x, y, z]) * r                                       # Scale to sphere radius

            shape = Shape(shape_name, shape_size)
            mesh = shape.create_3D_mesh()
            mesh.apply_translation(pos)
            scene.add_geometry(mesh)

    else:
        raise ValueError("3D mesh not supported for formation {formation}")
    
    return scene