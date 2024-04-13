import os
import uuid

import numpy as np
from imageio import imread

def multi_channel_conversion(files_path, channels_numbers):
    os.chdir(files_path)
    files = sorted(os.listdir(files_path), key = str.lower)
    try:
        len(files) % channels_numbers != 0
    except NameError:
        print(f"Something wrong with the file number, not multiples of {channels_numbers}")
    else:
        os.mkdir("multichannel_output")
        block_size = channels_numbers
        array_list = []
        round = 0
        for i in range(0, len(files), block_size):
            block_files = files[i:i + block_size]
            array_list.clear()
            for im in block_files:
                img = imread(im)
                array = np.asarray(img)
                array_list.append(array)
            random_uuid = str(uuid.uuid4())
            stacked_array = np.stack(array_list, axis=2)
            transposed_array = np.transpose(stacked_array, (2, 0, 1))
            file_name = block_files[0]
            file_name = file_name[:-10]
            metadata_header = f""" 
                                    <Image ID="Image:{round}" Name="{file_name}.tiff">
                                        <Pixels DimensionOrder="XYCTZ" ID="Pixels:{round}"  
                                            SignificantBits="8" SizeC="12" SizeT="1" SizeX="120" SizeY="70" SizeZ="1" Type="uint8">
                                            <Channel ID="Channel:{round}:0" 
                                            AcquisitionMode="BrightField"/>
                                            <Channel ID="Channel:{round}:1" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "488" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "528" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural" 
                                            Color = "65280"/>
                                            <Channel ID="Channel:{round}:2" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "488" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "577" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-65281"/>
                                            <Channel ID="Channel:{round}:3" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "488" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "610" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-2686721"/>
                                            <Channel ID="Channel:{round}:4" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy"  
                                            ExcitationWavelength = "488" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "702" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-16777216"/>
                                            <Channel ID="Channel:{round}:5" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "762" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "785" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Scattering"
                                            Color = "-8052199"/>
                                            <Channel ID="Channel:{round}:6" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "561" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "457" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-8388480"/>
                                            <Channel ID="Channel:{round}:7"
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy"   
                                            ExcitationWavelength = "561" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "537" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "65280"/>
                                            <Channel ID="Channel:{round}:8"
                                            AcquisitionMode="BrightField" Color="-1"/>
                                            <Channel ID="Channel:{round}:9" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "561" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "610" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-2686721"/>
                                            <Channel ID="Channel:{round}:10" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "561" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "702" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-16777216"/>
                                            <Channel ID="Channel:{round}:11" 
                                            AcquisitionMode="FluorescenceCorrelationSpectroscopy" 
                                            ExcitationWavelength = "561" 
                                            ExcitationWavelengthUnit="nm" 
                                            EmissionWavelength = "762" 
                                            EmissionWavelengthUnit="nm"
                                            Fluor="Natural"
                                            Color = "-8052199"/>
                                                <TiffData FirstC="0" FirstT="0" FirstZ="0" IFD="0" PlaneCount="1">
                                                    <UUID FileName="{file_name}.tiff">
                                                    urn:uuid:{random_uuid}
                                                    </UUID>
                                                </TiffData>
                                        </Pixels>
                                    </Image>"""
            tifffile.imwrite(f'multichannel_output/{file_name}.tiff',
                             transposed_array,
                             dtype=transposed_array.dtype,
                             shape=transposed_array.shape,
                             metadata={'axes': 'CYX'},
                             description=f"""<OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06 
                http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd" UUID="urn:uuid:{random_uuid}" 
                Creator="tifffile --v tifffile 2023.7.10">""" + metadata_header + """</OME>""")
            round += 1
