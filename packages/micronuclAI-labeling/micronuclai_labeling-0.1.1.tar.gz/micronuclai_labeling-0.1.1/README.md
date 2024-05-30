# micronuclAI labeling tool
[![PyPI](https://img.shields.io/pypi/v/micronuclAI_labeling?style=flat-square)](https://pypi.org/project/micronuclAI_labeling/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/micronuclAI_labeling?style=flat-square)](https://pypi.org/project/micronuclAI_labeling/)
[![PyPI - License](https://img.shields.io/pypi/l/micronuclAI_labeling?style=flat-square)](https://pypi.org/project/micronuclAI_labeling/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/micronuclAI_labeling?style=flat-square)](https://pypi.org/project/micronuclAI_labeling/)

## Installation
On your preferred python environment, run the following command:

``` bash
pip install micronuclAI-labeling
```
## Usage

To launch micronuclAI labeling tool, run the following command:

``` bash
python -m micronuclai_labeling --input path/to/image --mask path/to/mask --out path/to/outfile.csv
```

Once the tool is launched, you can use the following keyboard shortcuts:

The tool works by pressing any of the keys from 0-9:

The key 0 for no micro-nuclei present.  
The keys 1-9 for the number of observed micro-nuclei in the image.  
The key r is used to go back one image (in case any labeling mistake occurs).  

**NOTE:** Labeling doesn't have to be done in one session, it can be resumed later on.  
**NOTE:** Once labeling is complete the tool will not initiate.  
**NOTE:** Output, Input and Mask paths are required and must be the same in order to resume labeling.

## License

micronuclAI labeling tool offers a dual licensing mode the [GNU Affero General Public License v3.0](LICENSE) - see [LICENSE](LICENSE) and [ESSENTIAL_LICENSE_CONDITIONS.txt](ESSENTIAL_LICENSE_CONDITIONS.txt)
