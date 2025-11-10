from pymol import cmd

def color_identical(ref, ref_color, targets_colors):
    """
    Aligns structures to a reference, colors them individually,
    and creates named selections for residues identical to the reference.
    """
    
    # 1. Set Reference Color
    print(f"Setting reference {ref} to {ref_color}.")
    cmd.color(ref_color, ref)

    for target, base_color in targets_colors.items():
        print(f"Processing {target}...")
        cmd.color(base_color, target)
        
        # Align and get raw data
        aln_obj = f"aln_{ref}_{target}"
        cmd.align(target, ref, object=aln_obj)
        matches = cmd.get_raw_alignment(aln_obj)
        
        # List to store matching residue selection strings
        conserved_resi_list = []
        # Set to track processed residues to avoid duplicates
        seen_residues = set()

        for match in matches:
            atom1, atom2 = match[0], match[1]
            
            # Ensure correct mapping between ref and target
            if atom1[0] == ref and atom2[0] == target:
                ref_idx, tgt_idx = atom1[1], atom2[1]
            elif atom2[0] == ref and atom1[0] == target:
                ref_idx, tgt_idx = atom2[1], atom1[1]
            else:
                continue

            # Get atom objects to check residue names
            try:
                ref_atom = cmd.get_model(f"{ref} and index {ref_idx}").atom[0]
                tgt_atom = cmd.get_model(f"{target} and index {tgt_idx}").atom[0]
            except IndexError:
                continue

            # Check identity. We only need to check one atom per residue (e.g., CA)
            if ref_atom.resn == tgt_atom.resn and tgt_atom.name == "CA":
                # Create a unique identifier for this residue
                res_unique_id = f"/{target}//{tgt_atom.chain}/{tgt_atom.resi}"
                
                if res_unique_id not in seen_residues:
                    conserved_resi_list.append(res_unique_id)
                    seen_residues.add(res_unique_id)

        # Clean up alignment object
        cmd.delete(aln_obj)

        # Create the named selection if matches were found
        if conserved_resi_list:
            sel_name = f"{target}_identical"
            # Join all residue identifiers with 'or' to create one big selection
            sel_string = " or ".join(conserved_resi_list)
            cmd.select(sel_name, sel_string)
            
            # Apply the reference color to this new selection
            print(f"Created selection '{sel_name}' with {len(conserved_resi_list)} residues.")
            cmd.color(ref_color, sel_name)
        else:
            print(f"No identical residues found for {target}.")

    print("Completed. Selections created in standard menu.")

cmd.extend("color_identical", color_identical)