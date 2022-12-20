# Revuppaal
This is the Backend repository for our 7th semester project at Aalborg University. It is to be used with the [frontend](https://github.com/NickDue/revuepal).

## Setup
The backend is tested on both Ubuntu 22.04, Ubuntu 22.10 and MacOS.
To run the backend the following software is needed
- minikube
- kubectl
- verifyta (from the uppaal binaries)

When the software is installed the verifyta binary must be placed in a folder named `verifyer` in the folder `exercise-verifier`, the exercises is to be put into a folder named `exercise` in the folder `exercise-provider` and an empty folder named èxercises` must also be made in the `exercise-verifier`.

To setup the program one must run the commands in the file `setup_minikube.sh`

To connect to the website one must create a new mapping the the computers hosts file, where the hostname from `ingress.yaml` should map to the ip found when executing the command `minikube ip`
