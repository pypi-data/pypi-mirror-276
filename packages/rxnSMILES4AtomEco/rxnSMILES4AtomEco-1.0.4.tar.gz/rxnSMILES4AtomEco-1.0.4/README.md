### Last update 28 May 2024

<!--- Swiss CHEESE: an additional layer as Chemical Hazard Evaluation and Enhancement Safety Engine --->


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)    

# Welcome to veriCAS

veriCAS, a python library package for verification of CAS numbers and SMILES for known GHS hazards. Additionally, CAS numbers are screened against a target list (e.g. safety-relevant, export control, peroxydes, known peroxyde formers, custom, ...). For new chemical compounds SMILES functional group matching for explosives hazards is available.

---
**Table of Contents**

- [Description](#bulb-description)
- [Usage](#flying_saucer-usage)
  * [Flowchart](#flowchart)
- [Installation](#octopus-installation)
  * [Examples](#examples)
  * [Support](#support)
- [License](#license)
- [Cite](#card_index-cite)

---
## Version
1.0.0: Initial release

## :bulb: Description
The veriCAS project is a Python library designed for verification and analysis of chemical compounds represented by their CAS (Chemical Abstracts Service) registry numbers and/or SMILES (Simplified Molecular Input Line Entry System) strings.

veriCAS aims to provide comprehensive information about chemicals, including their structural formulas, IUPAC names and safety classifications according to the Globally Harmonized System of Classification and Labelling of Chemicals (GHS). The main output being the GHS hazard pictograms and GHS azard statements.

## :flying_saucer: Usage:
The veriCAS Python library is used as a tool for chemists, researchers, and professionals working with chemical compounds to verify their safety-relevant data, retrieve essential information, and analyze the safety classifications of compounds according to the internationally recognized standard GHS.

Here's an overview of its main functionalities:

###  Validation:
Validates the format and existance of input CAS numbers and SMILES strings.

### Information Retrieval
Retrieves chemical compound information such as canonical and isomeric SMILES, IUPAC names, safety classifications (GHS), and matches based on target list and specific functional groups.

### Data Querying
Queries database PubChem to fetch safety classification information and additional details about chemical compounds.

### Output Generation
Generates a summary report containing detailed information about chemical compounds, including structural formulas, names, GHS safety classifications, and any matches found based on list and functional groups entries.

### Flowchart

![veriCAS flowchart](./figsGHS/veriCAS.png "veriCAS flowchart.")

## :octopus: Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install veriCAS
```

### Examples

```python
import veriCAS

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

### Support
For help, issue tracker and wishes write to the main veriCAS developers.

<!--- ### Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README. --->

### Authors and acknowledgment
Appreciation to those who have contributed to the project:

- Dr. Simone Baffelli
- Dr. Samuele Giani

## License

[GPLv3.0 License](https://www.gnu.org/licenses/gpl-3.0) (aka GNU General Public License v3.0)

## :card_index: Cite
```
@article{foobar,
  title = {foobar},
  author = {Baffelli, Simone and Giani, Samuele},
  journal = {foobar},
  pages = {foobar},
  publisher = {foobar}
}
```
## Empa - Swiss Federal Laboratories for Materials Science and Technology


                                                  lrc
                                             *lllllllllc
                                         lrllllrrrllrrllllr
                                     rlllllrrrlllllllllrrrllll
                                *rlllllrrrlllllllllllllllllrrlllr}
                                xclrrrlllllllllllllllllllllllrrrlcv
                        rllllll vx%xcllllllllllllllllllllllllcx%vvi rlll
                   illllllrrrrllc%%%%%xclllllllllllllllllc%vviiiv%xlllrlllr
               rlllllrrrlllllllrrlcx%%%%%xcllllllllllc%viiiiv%xcllrrllllrrlllrs
           clllllrrrlllllllllllllllllcx%%%%%xclllc%viiiiv%xclllllllllllllllrrlllll
       vlrlllrrrllllllllllllllllllllllllcx%%%%%viiiiv%xcllllllllllllllllllllllrrlllll
       v%lllllllllllllllllllllllllllllllcx%%%%%viivclrrllllllllllllllllllllllllllrrrlxi
        %x%xclllllllllllllllllllllllcx%viii%xxc%iiv%%ccllllllllllllllllllllllllllcx%v%i
        x%%%%%clllllllllllllllllcx%viiiiv%clllllc%v%%%%%cclllllllllllllllllllcx%viiiivi
         %x%%%%%xcllllllllllcx%viiiivv%clllllllllllcc%%%%%%ccllllllllllllcx%viiiiiiiivi
         %%%%%%%%%%xclllcx%viiivv%cl*tw4PCIlll?uSEJ?rlcx%%%%%%cllllllcx%viiiiiiiiiiiivi
          %x%%%%%%%%%%viiiiv%xcllll}SBQQQQD4SOWQQQRPellllcx%%%%%%cx%viiiiiiiiiiiiiiiivi
          %%%%%%%%%%%%viivcllllllllll[hMQQQQQQQWVL?rllllllrlc%%%%%viiiiiiiiiiiiiiiiiivi<
           %cx%%%%%%%%%iivxcclllll!JgkDQQQMQQQQR&parllllllc%vv%%%%%iiiiiiiiiiiiiiiiiivii
           v%%%%%%%%%%%vii%%%xcllle4WQM&hT[ugBQ0KPC{llc%viiiii%%%%%iiiiiiiiiiiiiiiiiivii
            cllc%%%%%%%%iiv%%%%%xcllIj[rlllll!Te{c%%viiiiiiiiiv%%%%viiiiiiiiiiiiiiivvvi"
            %ccllcx%%%%%viv%%%%%%%%ccllllllllcxvvviiiiiiiiiiiiv%%%%viiiiiiiiiiiiv%clrrc%
            %%%%xlllx%%%vii%%%%%%%%%%xclllcx%viiiiiiiiiiiiiiiiv%%%%viiiiiiiiv%cllrlc%%%i
             %x%%%xcllcx%iiv%%%%%%%%%%%%%viiiiiiiiiiiiiiiiiiiiix%%%viiiiv%xclrlcx%viiivi
             %%x%%%%%clllxcc%%%%%%%%%%%%viiiiiiiiiiiiiiiiiiiiiiclcx%v%xclrllx%viiiiiiivi
              %x%%%%%%%xclllx%%%%%%%%%%%%viiiiiiiiiiiiiiiiiiiiivcllllrllc%viiiiiiiiiiivi
              v%%%%%%%%%%%%iiv%%%%%%%%%%%viiiiiiiiiiiiiiiiiiivv%%%xccx%viiiiiiiiiiiiiivi>
               %c%%%%%%%%%viivclc%%%%%%%%%iiiiiiiiiiiiiiiv%xclcx%%%%viiiiiiiiiiiiiiiiiviv
               %%%x%%%%%%%%iivxcllcx%%%%%%viiiiiiiiiiv%xclrllc%v%%%%viiiiiiiiiiiiiiiiivii
                 %%%xx%%%%%vii%%%xcllc%%%%viiiiiiiv%clrrlcxvviiiv%%%viiiiiiiiiiiiiivvviii
                   i%%%x%%%%iiv%%%%%cllcx%%iiiv%cllrlcx%viiiiiiiv%%%%iiiiiiiiiiivvviiiv%
                      %%%x%%viv%%%%%%%xcllc%xclrllx%viiiiiiiiiiiv%%%%iiiiiiivvviiiii
                        x%%x%iv%%%%%%%%%%cllllc%viiiiiiiiiiiiiiii%x%%viiivvviiiii
                          i%%viv%%%%%%%%%%%xvviiiiiiiiiiiiiiiiiivi%%xvvviiiii
                             % %%x%%%%%%%%%%iiiiiiiiiiiiiiiiiiiivi v%%iiv
                                %%%x%%%%%%%%viiiiiiiiiiiiiiiiivvvi>
                                 >%%%x%%%%%%%iiiiiiiiiiiiivvviiii>
                                    %%%xx%%%%viiiiiiiiivvviivii
                                      v%%%x%%viiiiivvviivvv
                                        c%%%x%ivvviiiii"
                                           %%%viiiiv
                                             vvv
