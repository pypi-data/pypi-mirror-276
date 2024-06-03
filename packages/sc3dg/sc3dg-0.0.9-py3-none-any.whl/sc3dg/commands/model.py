from sc3dg.model.STARK_nuc_dynamics import calc_genome_structure
from time import time
import argparse
def generate_3d( pair_file_path:str,
                pdb_file_path:str,
                num_models:int, 
                iter_steps:int,
                iter_res:list):

    # Number of alternative conformations to generate from repeat calculations
    # with different random starting coordinates
    num_models = num_models

    # Parameters to setup restraints and starting coords
    general_calc_params = {'dist_power_law': -0.33,
                           'contact_dist_lower': 0.8, 'contact_dist_upper': 1.2,
                           'backbone_dist_lower': 0.1, 'backbone_dist_upper': 1.1,
                           'random_seed': int(time()), 'random_radius': 10.0}

    # Annealing & dyamics parameters: the same for all stages
    # (this is cautious, but not an absolute requirement)
    anneal_params = {'temp_start': 5000.0, 'temp_end': 10.0, 'temp_steps': 100,
                     'dynamics_steps': iter_steps, 'time_step': 0.001}
                     # ynamics_step 精细度
    # Hierarchical scale protocol: calculations will initially use 8 Mb particles
    # but deminish to 100 kb at the end. The whole annealing protocol (hot to cold)
    # will be run at each size, but subsequent stages will start from the previous
    # structure
    # particle_sizes = [8e6, 4e6, 2e6, 4e5, 2e5, 1e5]
    particle_sizes =  iter_res
    # Contacts must be clustered with another within this separation threshold
    # (at both ends) to be considered supported, i.e. not isolated
    # This removes noise contacts
    isolation_threshold = 2e6

    Target_Chrom = ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12',
                    'chr13', 'chr14', 'chr15', 'chr16',
                    'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX']




    # Actually run the calculation with the specified parameters and input
    # The below function will automatically create the appropriate distance restraints
    calc_genome_structure(pair_file_path, pdb_file_path, general_calc_params, anneal_params,
                          particle_sizes, num_models, isolation_threshold, Target_Chrom=Target_Chrom, out_format='pdb')



def model():
    '''
        pair_file_path,
            pdb_file_path
            num_models:int, 
            iter_steps:int=10,
            iter_res:list=[8e6, 4e6, 2e6, 4e5, 2e5, 1e5]
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--pair',  help='pair path',required=True,
                        default=None)
    parser.add_argument('--pdb', help='pdb path',required=True, default=None)
    parser.add_argument('--num_models', help='num_models',required=False, default=5)
    parser.add_argument('--iter_steps', help='iter_steps',required=False, default=10)
    parser.add_argument('--iter_res', help='iter_res',required=False, default=[8e6, 4e6, 2e6, 4e5, 2e5, 1e5])
    
    
    args = parser.parse_args()
    generate_3d(args.pair, args.pdb, args.num_models, args.iter_steps, args.iter_res)