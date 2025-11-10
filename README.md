
# PyMOL Color-by-Identity Utility

A PyMOL script that automates the process of structurally aligning multiple proteins to a reference and highlighting residues that share strictly conserved sequence identity with that reference.

This tool is particularly useful for visually analyzing homologous families, isoforms, or closely related allergen structures to instantly identify conserved surface patches or core residues in 3D space.

## Features

  * **Automated Alignment:** Performs sequence-based structural alignment of all target proteins to a single reference protein.
  * **Identity Highlighting:** Identifies residues in target proteins that are identical to the reference at the aligned position.
  * **Customizable Coloring:** Allows the user to define a unique base color for every protein, while overriding identical residues with the reference color.
  * **Selection Generation:** Automatically creates named PyMOL selections (e.g., `protein2_identical`) containing only the conserved residues for easy subsequent manipulation (hiding, showing sticks, etc.).

## Prerequisites

  * **PyMOL:** This script must be run inside standard PyMOL (Open Source or Incentive builds).

## Installation

1.  Download `color_by_identity.py` from this repository.
2.  Save it to a known location on your computer.

## Usage

### 1\. Load the script

Open PyMOL and load the script using one of these methods:

  * **GUI:** Go to `File > Run Script...` and select `color_by_identity.py`.
  * **Command Line:** Type `run /path/to/color_by_identity.py` in the PyMOL command prompt.

### 2\. Run the command

The script adds a new function `color_identical` to the PyMOL namespace.

```python
color_identical(reference, reference_color, {targets_dict})
```

#### Arguments:

  * `reference` (string): The name of the object you want to serve as the master standard for alignment and coloring.
  * `reference_color` (string): The PyMOL color name for the reference protein (and identical residues in targets).
  * `targets_dict` (dictionary): A Python dictionary mapping target object names to their desired base colors.
      * *Syntax:* `{"object_name": "color_name", "object_name_2": "color_name_2"}`

## Example

Suppose you have three proteins loaded in PyMOL named `protein_A` (your reference), `protein_B`, and `protein_C`.

You want `protein_A` to be **red**. You want `protein_B` to be **blue**, and `protein_C` to be **green**, *unless* their residues exactly match `protein_A`, in which case they should also be **red**.

Run the following in the PyMOL command line:

```python
color_identical("protein_A", "red", {"protein_B": "blue", "protein_C": "green"})
```

### Output Results

After running the command:

1.  All proteins are aligned to `protein_A`.
2.  `protein_A` is colored red.
3.  `protein_B` is colored blue, but all residues identical to `protein_A` are recolored red.
4.  A new selection named `protein_B_identical` appears in the right-hand menu, containing only those red residues.
5.  (Same process applies to `protein_C`).

## How it Works

The script uses PyMOL's API to:

1.  Perform a `cmd.align` between targets and the reference.
2.  Extract the raw alignment data, which pairs atom indices between structures.
3.  Iterate through these pairs, checking if the residue names (e.g., TRP, ALA) match exactly.
4.  If they match, the residue is added to a custom selection and recolored.
