# Nuclear Health Effects Classifier
Nuclear Health Effects Classifier is an open-source classifier developed to predict survival and cancer rates from exposure to radiation >= 250mSv.

## Purpose

This classifier was developed as part of an undergraduate proposal to demonstrate the benefits of updating our atomic incident response technologies to the 21st century. It has been released to the public in the hope that it may prove useful. The proposal paper this classifier was developed for is also provided herein.

## How To Use

Simply clone the repository and run the source code:

```bash
git clone https://github.com/NoahGWood/NuclearHealthEffectsClassifier.git
cd NuclearHealthEffectsClassifier
./main.py
```

## Weights

A full set of trained weights is provided in the full_weights file. This script generates a set of weights using training data. The default setting creates weights based on randomly selected samples from the Hiroshima and Nagasaki database, to create weights based on the full training data, comment line #102 and uncomment line #103.  Weights are stored in a file 'weights' as a comma separated value of lists formatted as such:
		[survival_classifier], [cancer_classifier], [solid_cancer_classifier], [hema_cancer_classifier], [leukemia_cancer_classifier]

## Acknowledgement

​	This report makes use of data obtained from Radiation Effects Research Foundation (RERF), Hiroshima and Nagasaki, Japan. RERF is a private, non-profit foundation funded by the Japanese Ministry of Health, Labour and Welfare and the U.S. Department of Energy, the latter through the National Academy of Sciences. The conclusions in this report are those of the authors and do not necessarily reflect the scientific judgment of RERF or its funding agencies.
