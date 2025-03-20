import numpy as np



def get_mesh_y_positions(cell_centres, nx, ny):
    # Getting cell centres, particularly Y positions
    print("Obtaining cell centres...")
    print(f"Cell centres: {cell_centres} and lenght is {len(cell_centres)}")
    y_cell_centres_repeated = cell_centres[:,1]
    print(f"Y cell centres repeated: {y_cell_centres_repeated} and lenght is {len(y_cell_centres_repeated)}")
    block_elements = int(len(y_cell_centres_repeated)/2)
    ny2 = int(ny/2)
    

    # Taking elements for the nodes of the first half of the channel separated nx, so that we
    # only get the ones at the inlet face. Then selecting the first ny/2 to select only one column
    y_cell_centres_1 = y_cell_centres_repeated[:block_elements:nx][:ny2]  
    y_cell_centres_2 = y_cell_centres_repeated[block_elements::nx][:ny2]
    y_cell_centres = np.concatenate((y_cell_centres_1, y_cell_centres_2))    

    print(f"Y cell centres: {y_cell_centres} and lenght is {len(y_cell_centres)}")

    return y_cell_centres