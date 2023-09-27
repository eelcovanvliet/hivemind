from __future__ import annotations
from .abstracts import Base, State
from .abstracts import Mesh, Inertia
from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import Dict, Tuple
from carg_io.abstracts import ParameterSet, Parameter, units
from gmsh_utils import utils
from gmsh_utils import mesh
import gmsh
import numpy as np
from pathlib import Path
# import meshmagick.mmio as mmio
import pandas as pd

class Structure(Base):

    """Describe a structural object, i.e. anything that has mass and some spatial properties."""

    @abstractmethod
    def get_ballast_tanks(self) -> pd.DataFrame:
        ...

    @abstractmethod
    def get_geometry(self) -> utils.VolumeComponent:
        ...
    
    @abstractmethod
    def get_inertia(self) -> Inertia:
        ...

    def get_mesh(self, file, mesh_size: float = 5, show=False):
        """Creates a mesh from the geometry defined

        Args:
            file (str): location to safe the file
            mesh_size (float, optional): size of mesh elements. Defaults to 5.
            show (bool, optional): open gui after mesh creation. Defaults to False.

        Raises:
            ValueError: error if file extensions does not match .msh

        Returns:
            mesh (list): the readed mesh fike
        """
        file = Path(file)
        if file.suffix != '.msh':
            raise ValueError(f'Expected a .msh extesions, got {file.suffix}')
        file = file.with_suffix('.msh')

        # Mesh surfaces
        mesh.mesh_surfaces(mesh_size)

        # Write mesh file and store content in instance.
        gmsh.write(str(file))
        with open(file, 'r') as f:
            self.mesh = f.read()

        if show:
            utils.ui.start_ui(mode='mesh')
        return self.mesh

    def cut_geometry(self, geometry: utils.VolumeComponent, draft: float, roll: float) -> Tuple[utils.AreaComponent, utils.VolumeComponent]:
        """Take the geometry and peforms a "cut" using a plane based on draft and roll

        NOTE:
            - cutting plane size currently set to 500 by 500 -> use of bounding box in future version

        Parameters:
            geometry:utils.VolumeComponent
                The geometry as returned by .get_geometry()
                NOTE: Asssumes origin of geometry at aft, centerline, keel

        Return:
            volumes_below_water_surface: utils.VolumeComponent
                Component containing the volumes below the water surface (cutting plane)
            water_crossing_surfaces: utils.AreaComponent
                Component containing the surfaces outlined by the sscv water line.

        """
        geometry.translate(dx=0, dy=0, dz=0).rotate(0, 0, 0, 1, 0, 0, np.deg2rad(roll))

        bmin, bmax = geometry.get_bounding_box()

        # Create slicing plane
        plane = utils.make_polygon([
            [bmin[0]*1.1,  bmin[1]*1.1,  draft],
            [bmax[0]*1.1,  bmin[1]*1.1,  draft],
            [bmax[0]*1.1,  bmax[1]*1.1,  draft],
            [bmin[0]*1.1,  bmax[1]*1.1,  draft],
            
        ])
        # Fragment (general fuse) geometry using plane
        water_crossing_surfaces = geometry.slice([plane])
        volume_below_water_surface = geometry[geometry.z < water_crossing_surfaces.z.max()]

        return volume_below_water_surface, water_crossing_surfaces    

    def get_geometry_below_waterplane(self, draft: float = 0, threshold: float = 0.001) -> utils.VolumeComponent:
        """Function to get the geometry below the water surface for exporting to GDF/WAMIT.

        NOTE:
            - Vessel roll assumed to be zero
            - Only returns surfaces -> no volume as the shape is open! (For WAMIT purpose)

        Args:
            draft (float, optional): Draft of vessel. Defaults to 0.
            threshold (float, optional): threshold for selecting the waterplane surface. Defaults to 0.001.

        Returns:
            utils.VolumeComponent: geometry 
                NOTE !!! I BELIEVE THIS RETURNS THE ORIGINAL GEOMETRY, NOT THE NEW ONE
        """
        geometry = self.get_geometry()

        volumes_below_water_surfaceTags, _ = self.cut_geometry(geometry, draft=draft, roll=0)

        volumesBelowWaterSurface = utils.VolumeComponent(dimTags=volumes_below_water_surfaceTags)
        AdjacenciesVolumeBelowWaterSurfaceTags = volumesBelowWaterSurface.get_adjacencies()

        # Get surfaces that need to be deleted
        AllSurfacesTags = gmsh.model.get_entities(dim=2)
        SurfacesToRemoveTags = []
        for surface_index, surface in enumerate(AllSurfacesTags):
            if surface[1] in AdjacenciesVolumeBelowWaterSurfaceTags[1]:
                pass
            else:
                SurfacesToRemoveTags.append(surface)

        SurfacesForMeshTags = []
        for surface in AdjacenciesVolumeBelowWaterSurfaceTags[1]:
            surface_cog = gmsh.model.occ.get_center_of_mass(2, surface)
            if surface_cog[2] >= draft - threshold:
                SurfacesToRemoveTags.append((2, surface))
            else:
                SurfacesForMeshTags.append((2, surface))

        SurfacesForMesh = utils.VolumeComponent(dimTags=SurfacesForMeshTags)

        # Delete volumes and surfaces
        AllVolumeTags = gmsh.model.get_entities(dim=3)
        AllVolumes = utils.VolumeComponent(dimTags=AllVolumeTags)
        AllVolumes.remove(recursive=False)

        SurfacesToRemove = utils.VolumeComponent(dimTags=SurfacesToRemoveTags)
        SurfacesToRemove.remove(recursive=True)  # Also delete corresponding lines

        # Translate geometry
        SurfacesForMesh.translate(dx=0, dy=0, dz=-draft)

        return SurfacesForMesh


    def export_mesh_to_gdf(self, file: str, draft: float, show=False):
        """Export generated .msh to .gdf

        NOTE:
            - Symmetry of the gdf file is set to 0 for Ix and Iy
            - assumed vessel draft is selected to 'cut' the mesh
            - Does not include any shift of vessel for draft setting
            - TODO Check if it is valid to change length scale from 100 to 1!

        Args:
            file (str): file name of gdf
            draft (float): draft of vessel for export to gdf
            show (bool, optional): if True show generated msh
        """
        file = Path(file)

        # Get geometry
        geometry = self.get_geometry_below_waterplane(draft=draft)

        # Create mesh
        temp_mesh_file_name = 'temp_msh_for_export_to_gdf.msh'
        self.get_mesh(temp_mesh_file_name, show=show, mesh_size=10)

        # Export mesh to gdf
        vertices, faces = mmio.load_MSH(temp_mesh_file_name)
        mmio.write_GDF(file, np.array(vertices), faces)

        # Update symmetry settings (set to zero symmetry)
        with open(file, 'r') as f:
            data = f.readlines()

        data[1] = '%16.6f%16.6f\n' % (1, 9.81)
        data[2] = '%12u%12u\n' % (0, 0)
        with open(file, 'w') as f:
            f.writelines(data)

        print(f'Exported gdf mesh to: {str(file)}')