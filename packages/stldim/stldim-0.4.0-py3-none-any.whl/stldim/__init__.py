"""
A module that provides a class that extends the stl.Mesh class to include properties for the mesh's
dimensions.
"""

import os
import re

import jinja2
import stl
from stl import mesh


class MeshWithBounds(mesh.Mesh):
    """
    A class that extends the stl.Mesh class to include properties for the mesh's dimensions.
    """

    @property
    def maxx(self):
        """Calculate and return the maximum x of the mesh."""
        return max(self.points, key=lambda p: p[stl.Dimension.X.value])[stl.Dimension.X.value]

    @property
    def minx(self):
        """Calculate and return the minimum x of the mesh."""
        return min(self.points, key=lambda p: p[stl.Dimension.X.value])[stl.Dimension.X.value]

    @property
    def maxy(self):
        """Calculate and return the maximum y of the mesh."""
        return max(self.points, key=lambda p: p[stl.Dimension.Y.value])[stl.Dimension.Y.value]

    @property
    def miny(self):
        """Calculate and return the minimum y of the mesh."""
        return min(self.points, key=lambda p: p[stl.Dimension.Y.value])[stl.Dimension.Y.value]

    @property
    def maxz(self):
        """Calculate and return the maximum z of the mesh."""
        return max(self.points, key=lambda p: p[stl.Dimension.Z.value])[stl.Dimension.Z.value]

    @property
    def minz(self):
        """Calculate and return the minimum z of the mesh."""
        return min(self.points, key=lambda p: p[stl.Dimension.Z.value])[stl.Dimension.Z.value]

    @property
    def xsize(self):
        """Calculate and return the size of the mesh in the x direction."""
        return round(self.maxx - self.minx, 3)

    @property
    def ysize(self):
        """Calculate and return the size of the mesh in the y direction."""
        return round(self.maxy - self.miny, 3)

    @property
    def zsize(self):
        """Calculate and return the size of the mesh in the z direction."""
        return round(self.maxz - self.minz, 3)

    @property
    def midx(self):
        """Calculate and return the midpoint of the mesh in the x direction."""
        return round(self.xsize / 2, 3)

    @property
    def midy(self):
        """Calculate and return the midpoint of the mesh in the y direction."""
        return round(self.ysize / 2, 3)

    @property
    def midz(self):
        """Calculate and return the midpoint of the mesh in the z direction."""
        return round(self.zsize / 2, 3)

    @property
    def dimensions(self):
        """Return a dictionary of the mesh's dimensions."""
        return {
            'min_x': round(self.minx, 3),
            'max_x': round(self.maxx, 3),
            'min_y': round(self.miny, 3),
            'max_y': round(self.maxy, 3),
            'min_z': round(self.minz, 3),
            'max_z': round(self.maxz, 3),
            'x_size': round(self.xsize, 3),
            'y_size': round(self.ysize, 3),
            'z_size': round(self.zsize, 3),
            'mid_x': round(self.midx, 3),
            'mid_y': round(self.midy, 3),
            'mid_z': round(self.midz, 3),
        }

    # pylint: disable=too-many-arguments
    def __init__(self, data, calculate_normals=True, name='', filename=None, varname=None,
                 **kwargs):
        super().__init__(data, calculate_normals=calculate_normals, name=name, **kwargs)
        self.filename = filename
        self._varname = varname

    # pylint: disable=too-many-arguments
    @classmethod
    def from_file(cls, filename, calculate_normals=True, fh=None, mode=stl.Mode.AUTOMATIC,
                  speedups=True, varname=None, **kwargs):
        """Load a mesh from a STL file and store the filename.

        Args:
            filename (str): The file to load.
            calculate_normals (bool, optional): Whether to update the normals (default: True).
            fh (file, optional): The file handle to open (default: None).
            mode (stl.mesh.Mode, optional): The STL file mode (default: stl.Mode.AUTOMATIC).
            speedups (bool, optional): Whether to use optimizations (default: True).
            kwargs: Additional keyword arguments passed to the Mesh constructor.

        Returns:
            MeshWithBounds: A new MeshWithBounds object with the loaded mesh data and filename.
        """

        if fh:
            name, data = cls.load(
                fh, mode=mode, speedups=speedups
            )
        else:
            with open(filename, 'rb') as fh: # pylint: disable=redefined-argument-from-local
                name, data = cls.load(
                    fh, mode=mode, speedups=speedups
                )
        return cls(
            data, calculate_normals, name=name, filename = filename,
            speedups=speedups, varname=varname, **kwargs
        )

    @property
    def sanitized_filename(self):
        """
        Replace every non-alphanumeric character with an underscore
        """

        sanitized = re.sub(r'\W', '_', os.path.basename(self.filename)).lower()
        match = re.search(r"\D", sanitized)
        if match:
            return "_" * (match.start()) + sanitized[match.start():]
        return sanitized

    @property
    def varname(self):
        """
        Return a sanitized variable name based on the filename or the provided name.
        """
        if self._varname:
            return self._varname
        return self.sanitized_filename

    def render(self, template):
        """
        Render the template with the mesh's dimensions
        """
        environment = jinja2.Environment(loader=jinja2.PackageLoader('stldim', 'templates'))
        template = environment.get_template(f'{template}.jinja2')
        return template.render(mesh=self)
