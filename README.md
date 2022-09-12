# Canonical assignment
## Wildfire cause Prediction

### Running the project
1. Create conda environment using `conda create -n <env name> python=3.9 pip`
2. Activate environment using `conda activate <env name>`
3. Install required libs using `pip install -r requirements.txt`
4. Place `FPA_FOD_20170508.sqlite` in the root project directory.
5. Finally, download the pickled model file from [here](https://drive.google.com/file/d/1vvBMoiIqGux0pYoZB-5VwDgtjDlSiI2P/view?usp=sharing), and place into the `assets` directory. Or run the notebook in order and it will be saved.

#### To run the notebook
- In root project directory run `jupyter lab` and run cells in the same order.

#### To run dashboard
- In root project directory run `streamlit run dashboard/Q1.py`
- Each question is in a seperate page, to be chosen from the left sidebar, specific instructions (if any) are in each respective page.