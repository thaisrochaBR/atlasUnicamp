# Labeled GOES-16 Satellite Images for River Inflow and Discharge Estimation

## Description
This dataset contains labeled satellite images acquired from the GOES-16 satellite and associated with river inflow and discharge measurements in the Tietê River basin, Brazil. The dataset was developed to support machine learning and deep learning applications in hydrological forecasting and remote sensing.

Each satellite image is linked to hydrological observations obtained from streamflow gauging stations, enabling supervised learning approaches for river inflow and discharge estimation.

The dataset includes preprocessed satellite images, metadata describing monitoring stations, and labels containing inflow and discharge values.

---

## Data Contents
- GOES-16 satellite images
- Hydrological labels (river inflow and discharge)
- Metadata describing streamflow gauging stations
- Station information file (`stations_info.csv`)

---

## Data Structure
```text
dataset/
├── images/          # GOES-16 satellite images
├── labels/          # CSV files with inflow and discharge values
├── metadata/        # Station metadata (stations_info.csv)
└── README.md
```
---

## Station Metadata
The file `stations_info.csv` provides metadata for the streamflow gauging stations used in this dataset, including:
- Station identifier and station code
- River basin and sub-basin
- Associated river
- Geographic location (latitude and longitude)
- Altitude and drainage area

Geographic coordinates are provided in degrees, minutes, and seconds (DMS), following the original records from the Brazilian National Water Agency (ANA).

To ensure compatibility across different operating systems, programming languages, and data processing tools, accented characters were removed from the CSV files.

---

## Intended Use
This dataset is intended for research and academic purposes, including but not limited to:
- Machine learning and deep learning applications
- Hydrological forecasting
- Remote sensing studies
- River inflow and discharge estimation

Users are encouraged to cite the dataset when used in scientific publications.

---

## Source Code
The Python source code used for satellite image acquisition, preprocessing, and dataset generation is publicly available at:

- GitHub repository: https://github.com/thaisrochaBR/atlasUnicamp 
- Zenodo (Software): DOI_TO_BE_ADDED

---

## License
This dataset is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.  
Users are free to share and adapt the material, provided appropriate credit is given.

---

## Citation
If you use this dataset in your research, please cite it as:

Rocha, T.; Angelis, A. F (2026). *Labeled GOES-16 Satellite Images for River Inflow and Discharge Estimation*. Zenodo. https://doi.org/XXXX

---

## Authors

**Thais Rocha¹***, **Andre Franceschi de Angelis²**

¹ School of Technology, University of Campinas (UNICAMP), Campinas, SP, Brazil  
Email: thaisrocl@unicamp.br  

² School of Technology, University of Campinas (UNICAMP), Campinas, SP, Brazil  
Email: andre@ft.unicamp.br  

\* Corresponding author: spthaisrocha@gmail.com
