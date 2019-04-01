# CSCI 8360 Data Science Practicum : Project NeuroFinder

  ## Goal
  To develop a segmentation pipeline that identifies as many neurons as possible, as accurately as possible.
  
  ## Getting Started
  These instructions describe the prerequisites and steps to get the project up and running.

  ### Prerequisites
  This project can be easily set up on the Google Cloud Platform, using a '[Deep Learning VM Instance](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/deeplearning)'. You will need to have [Google Cloud SDK](https://cloud.google.com/sdk/install) installed in your local machine to be able to set the project up.

  After downloading/cloning this repository to your local machine, the user will need to open the `Google Cloud SDK Shell`. Once it opens, the user can copy the contents of this repository to the Deep Learning VM instance using the command:

  `gcloud compute scp --recurse /complete/link/to/repository/* <user>@<instance_name-vm>:/home/<user>/`

  The Deep Learning VM instance is a good place to deploy this project, because it comes pre-installed with a majority of the packages used in this project, such as, 'OpenCV', 'Tensorflow', 'Keras', 'Matplotlib', 'Sklearn', 'Skimage', and 'Numpy'. The packages that are installed through the DataLoader class upon spinning up the project include 'thunder-extraction' and 'pytest'.

  ### Usage
  To run the code and generate output prediction masks in the `/results` directory, the user can navigate to the folder containing the file 'team-hopper.py', and run it using the command: `python team-hopper.py --options`. The user can get a description of the options by using the command `python team-hopper.py -help`.
  
  ### Dataset
  The dataset was created by (codeneuro.org)[http://codeneuro.org/]. 
  ![alt text](http://url/to/img.png) ![alt text](http://url/to/img.png)
  The image on the left is a training example and on the right is the mask with the regions circled.
  
  ### Output
  Upon running the command in the ‘Usage’ section, the dataset will be downloaded from the Google Storage bucket link carrying the Neuron dataset, and the output `submission.json` files will be generated in the `/results` directory.

  ## Contributors
* See [Contributors](CONTRIBUTORS.md) file for more details.

## License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for more details.
