## The Chase

The Chase is a fundamental algorithm in databases for testing entailment of integrity constraints such as functional dependencies, multivalued dependencies and lossless join. Our project implements the chase algorithm. We also define an XML format for the problem statements and generate traces in an XML format.


## Getting Started

To get a local copy up and running follow these simple example steps.


### Prerequisites

You will need to have python3 installed. The project is developed with version 3.10.9.


### Installation
1. Clone the repo
    ```sh
    git clone https://github.com/tanruiquan/cs4221-project-chase.git
    ```
2. `cd` into the root directory
    ```sh
    cd cs4221-project-chase
    ```


## Usage

To use the application, run the following command in the terminal
```zsh
python3 main.py [chase_type] path_to_input_file [path_to_output_file]
```
- main.py: the application that implements the chase algorithm
- chase_type: the version of chase to use, supports `simple` and `distinguished` chase (default to `distinguished`)
- path_to_input_file: the path to an xml file that describe the problem statement
- path_to_output_file: the path to an xml file that the result will be written to (default to `output.xml`)

### Example 
To test for the entailment of functional dependency.
```sh
python3 main.py distinguished examples/functional_dependency1.xml outputs/functional_dependency1.xml
```
