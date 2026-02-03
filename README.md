# GOES Satellite Images and Streamflow Dataset for Hydrological Forecasting

This repository contains source codes, notebooks, and auxiliary files used for the **collection, processing, and organization of a large dataset of GOES satellite images**, as well as their **integration with river inflow and discharge data**, with a focus on **hydrological modeling and streamflow forecasting applications**.

The material was prepared to support **research activities** and the **publication of the associated dataset on Zenodo**, ensuring reproducibility, transparency, and adherence to open science best practices.

---

## 📂 Repository Structure

```
├── app_get_images_goes.py          # Script for GOES image download
├── app_get_images_goesv2.py        # Improved version of the GOES download script
├── app_merge_img_inflow.ipynb      # Notebook for image–streamflow data integration
├── requirements.txt                # Python environment dependencies
├── README.md                       # This file
```

In addition to these files, the **final dataset** consists of approximately **27,000 satellite images**, which are stored and made available separately via **Zenodo** due to their large volume.

---

## 🛰️ Satellite Data (GOES)

The images used in this research are obtained from the **GOES (Geostationary Operational Environmental Satellites)** program, widely employed in meteorological and hydrological studies.

The scripts `app_get_images_goes.py` and `app_get_images_goesv2.py` perform the following tasks:

* Access public GOES data sources;
* Automated download of satellite images;
* Organization of images by date and time;
* Standardization of file names and directory structure.

These images are subsequently used as **visual inputs** for machine learning models applied to streamflow forecasting.

---

## 🌊 Streamflow Data

Streamflow data used in this research are integrated with the satellite images using the following notebook:

* `app_merge_img_inflow.ipynb`

This notebook is responsible for:

* Loading streamflow time series;
* Temporally synchronizing GOES images with hydrological observations;
* Generating image–streamflow pairs suitable for model training and validation;
* Exporting the final datasets used in the experiments.

---

## ⚙️ System Requirements

Project dependencies are listed in the `requirements.txt` file.

To create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/binactivate  # Linux/Mac
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
```

Python **3.9 or later** is recommended.

---

## 🚀 Recommended Workflow

1. **Install dependencies** using `requirements.txt`;
2. **Run the download scripts** (`app_get_images_goes.py` or `app_get_images_goesv2.py`);
3. **Organize satellite images** into date-based directories;
4. **Execute the notebook** `app_merge_img_inflow.ipynb` to integrate images with streamflow data;
5. **Generate the final dataset**, which is used in the experiments and published on Zenodo.

---

## 📦 Dataset Publication on Zenodo

Due to the large data volume (approximately **27,000 images**), the complete dataset is published on **Zenodo**, which provides:

* A persistent DOI;
* Dataset versioning;
* Open access and long-term preservation.

The dataset of labeled GOES-16 satellite images used in this research is publicly available in Zenodo and should be cited in publications according to the journal or conference guidelines.

---

## 🧩 Source Code Availability

The Python source code used for satellite image acquisition, preprocessing, and dataset generation is publicly available at:

* **GitHub repository:** [https://github.com/thaisrochaBR/atlasUnicamp](https://github.com/thaisrochaBR/atlasUnicamp)
* **Zenodo (Software):** [https://doi.org/10.5281/zenodo.18471522](https://doi.org/10.5281/zenodo.18471522)

---

## 👩‍🔬 Authorship and Credits

**Thais Rocha**
University of Campinas (UNICAMP)
Postdoctoral Researcher in Artificial Intelligence Applied to Hydrology

**Andre Franceschi de Angelis**
University of Campinas (UNICAMP)

---

## 📜 License

This project is released under the **MIT License**, which permits use, copy, modification, distribution, and private or commercial use, provided that the original authors are properly credited.

Copyright (c) 2026 Thais Rocha, Andre Franceschi de Angelis

---

## 📬 Contact

For questions, suggestions, or academic collaborations, please contact the author using the information provided in the associated scientific publications.
