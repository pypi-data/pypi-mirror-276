import glob
import numpy as np
import pandas as pd
import subprocess
import os

from config import DATA_DIR, SCRIPTS_DIR, STRUCTURES_DIR
from utils.generic_utils import noABC

class Preprocessing(object):
    """
    Preprocessing class. It generates the residue normal mode correlation maps.
    
    """

    def __init__(
            self,
            data_path=DATA_DIR,
            scripts_path=SCRIPTS_DIR,
            structures_path=STRUCTURES_DIR,
            df='sabdab_summary_all.tsv',
            modes=30,
            chain_lenghts_path='chain_lengths/',
            dccm_map_path='dccm_maps/',
            residues_path='lists_of_residues/',
            file_type_input='.pdb',
            selection='_CDR1_to_CDR3',
            pathological=None,
            renew_maps=False,
            renew_residues=False,
    ):
        """
        :param data_path: path to the data folder
        :type data_path: str
        :param scripts_path: path to the scripts folder
        :type scripts_path: str
        :param structures_path: path to the PDB files
        :type structures_path: str
        :param df: name of the database containing the PDB entries
        :type df: str
        :param modes: number of considered normal modes
        :type modes: int
        :param chain_lenghts_path: path to the folder containing arrays with the chain lenghts
        :type chain_lenghts_path: str
        :param dccm_map_path: path to the normal mode correlation maps
        :type dccm_map_path: str
        :param residues_path: path to the folder containing the list of residues per entry
        :type residues_path: str
        :param file_type_input: filename extension of input structures
        :type file_type_input: str
        :param selection: considered portion of antibody chains
        :type selection: str
        :param pathological: list containing the PDB identifiers of antibodies that need to be excluded
        :param renew_maps: compute all the normal mode correlation maps
        :type renew_maps: bool
        :param renew_residues: retrieve the lists of residues for each entry
        :type renew_residues: bool

        """
        self.data_path = data_path
        self.scripts_path = scripts_path
        self.structures_path = structures_path
        self.df_path = data_path + df
        self.chain_lenghts_path = chain_lenghts_path
        self.dccm_map_path = data_path + dccm_map_path
        self.residues_path = data_path + residues_path
        self.modes = modes
        self.file_type_input = file_type_input
        self.selection = selection
        self.pathological = pathological

        self.entries, self.affinity, self.df = self.clean_df()
        self.h_length, self.l_length, self.selected_entries = self.initialisation(renew_maps, renew_residues)
        self.max_res_list_h, self.max_res_list_l, self.min_res_list_h, self.min_res_list_l = self.get_max_min_chains()

    def clean_df(self):
        """
        Cleans the database containing the PDB entries.

        :return: a list of the PDB entries, a list of the binding affinities and the underlying database

        """

        df = pd.read_csv(self.df_path, sep='\t', header=0)[['pdb', 'antigen_type', 'affinity']]
        df.drop_duplicates(keep='first', subset='pdb', inplace=True)
        df = df[(df.antigen_type.notna()) & (df.antigen_type != 'NA')][['pdb', 'affinity']]
        df = df[(df.affinity.notna()) & (df.affinity != 'None')]
        df = df[~df['pdb'].isin(self.pathological)] # Removing pathological cases 

        return list(df['pdb']), list(df['affinity']), df

    def generate_cdr1_to_cdr3_pdb(self, path, keepABC=True, lresidues=False, hupsymchain=None, lupsymchain=None):
        """
        Generates a new PDB file going from the beginning of the CDR1 until the end of the CDR3.

        :param path: path of a Chothia-numbered PDB file 
        :type path: str
        :param keepABC: keeps residues whose name ends with a letter from 'A' to 'Z'
        :type keepABC: bool
        :param lresidues: the names of each residue are stored in ``self.residues_path``
        :type lresidues: bool
        :param hupsymchain: upper limit of heavy chain residues due to a change in the numbering convention. Only useful when using ``AlphaFold``
        :type hupsymchain: int
        :param lupsymchain: upper limit of light chain residues due to a change in the numbering convention. Only useful when using ``AlphaFold``
        :type lupsymchain: int

        """
        list_residues = ['START']
        with open(path, 'r') as f: # needs to be Chothia-numbered
            content = f.readlines()
            header_lines_important = range(4)
            header_lines = [content[i][0]=='R' for i in range(len(content))].count(True)
            h_range = range(26, 103)
            l_range = range(24, 98)
            start_chain = 21
            chain_range = slice(start_chain, start_chain+1)
            res_range = slice(23, 26)
            res_extra_letter = 26 #sometimes includes a letter 'A', 'B', 'C', ...
            h_chain_key = 'HCHAIN'
            l_chain_key = 'LCHAIN'
            idx_list = list(header_lines_important)
            idx_list_l = []
            new_path = path[:-4] + self.selection + path[-4:]
            
            # Getting the names of the heavy and light chains
            line = content[header_lines_important[-1]]
            if line.find(h_chain_key) != -1:
                h_pos = line.find(h_chain_key) + len(h_chain_key) + 1
                h_chain = line[h_pos:h_pos+1]
            else:
                # useful when using AlphaFold
                h_chain = 'A' 
                l_chain = 'B'
                idx_list = [0]
                h_range = range(26, hupsymchain)
                l_range = range(24, lupsymchain)
                
            if line.find(l_chain_key) != -1:
                l_pos = line.find(l_chain_key) + len(l_chain_key) + 1
                l_chain = line[l_pos:l_pos+1]
            else: 
                l_chain = None
                
            # Checking if H and L chains have the same name
            if l_chain is not None and h_chain.upper() == l_chain.upper():
                pathologic = True
                h_chain = h_chain.upper()
                l_chain = h_chain.lower()
                print(content[0])
            else:
                pathologic = False
                
            # Obtaining the CDR1 to CDR3 lines for both chains
            for i, line in enumerate(content[header_lines:]):
                if line[chain_range].find(h_chain) != -1 and int(line[res_range]) in h_range:
                    if line[res_extra_letter] == ' ' or keepABC == True:
                        idx_list.append(i+header_lines)
                        if lresidues == True:
                            full_res = line[res_range] + line[res_extra_letter]
                            if pathologic:
                                full_res = 'A' + full_res
                            else:
                                full_res = line[chain_range] + full_res
                            if full_res != list_residues[-1]:
                                list_residues.append(full_res)

            # This separation ensures that heavy chain residues are enlisted first
            if l_chain is not None:
                for i, line in enumerate(content[header_lines:]):
                    if line[chain_range].find(l_chain) != -1 and int(line[res_range]) in l_range:
                        if line[res_extra_letter] == ' ' or keepABC == True:
                            idx_list_l.append(i+header_lines)
                            if lresidues == True:
                                full_res = line[res_range] + line[res_extra_letter]
                                if pathologic:
                                    full_res = 'B' + full_res
                                else:
                                    full_res = line[chain_range] + full_res
                                if full_res != list_residues[-1]:
                                    list_residues.append(full_res)                   
        
        # List with name of every residue is saved if selected
        if lresidues == True:
            list_residues.append('END')
            np.save(self.residues_path + path[-8:-4] + '.npy', list_residues)
                                        
        # Creating new file
        with open(new_path, 'w') as f_new:
            if pathologic:
                new_hchain = 'A'
                new_lchain = 'B'
            else:
                new_hchain = h_chain
                new_lchain = l_chain
            f_new.writelines([content[l] for l in idx_list[:header_lines_important[-1]]])
            if l_chain is not None:
                f_new.writelines([content[l][:h_pos]+new_hchain+content[l][h_pos+1:l_pos]+new_lchain+content[l][l_pos+1:] for l in idx_list[header_lines_important[-1]:header_lines_important[-1]+1]])
            else:
                f_new.writelines([content[l][:h_pos]+new_hchain+content[l][h_pos+1:] for l in idx_list[header_lines_important[-1]:header_lines_important[-1]+1]])
            f_new.writelines([content[l][:start_chain]+new_hchain+content[l][start_chain+1:] for l in idx_list[header_lines_important[-1]+1:]])
            if l_chain is not None:
                f_new.writelines([content[l][:start_chain]+new_lchain+content[l][start_chain+1:] for l in idx_list_l])

    def generate_maps(self):
        """
        Generates the normal mode correlation maps.

        """
        for entry in self.entries:
            file_name = entry + self.selection
            path = self.structures_path + file_name + self.file_type_input
            new_path = self.dccm_map_path + entry
            self.generate_cdr1_to_cdr3_pdb(self.structures_path+entry+self.file_type_input) 
            subprocess.call(['/usr/local/bin/RScript '+str(self.scripts_path)+'pdb_to_dccm.r '+str(path)+' '+str(new_path)+' '+str(self.modes)], shell=True, stdout=open(os.devnull, 'wb'))
        
            if os.path.exists(path):
                os.remove(path)

    def get_lists_of_lenghts(self, selected_entries):
        """
        Retrieves lists with the lenghts of the heavy and light chains.
        :param selected_entries: list of valid entries

        """
        heavy = []
        light = []

        for entry in selected_entries:
            file_name = entry + self.selection
            path = self.structures_path + file_name + self.file_type_input
            self.generate_cdr1_to_cdr3_pdb(self.structures_path+entry+self.file_type_input, keepABC=True, lresidues=True)
            subprocess.call(['/usr/local/bin/RScript'+str(self.scripts_path)+'get_chain_lengths.r '+str(path)], shell=True, stdout=open(os.devnull, 'wb'))
           
            if os.path.exists(path):
                os.remove(path)
            h, l = np.load('/Users/kevinmicha/Downloads/value.npy') # there might be a neat solution
        
            heavy.append(h)
            light.append(l)
        
        np.save(self.chain_lenghts_path+'heavy_lengths.npy', heavy)
        np.save(self.chain_lenghts_path+'light_lengths.npy', light)
        np.save(self.chain_lenghts_path+'selected_entries.npy', selected_entries)

    def get_max_min_chains(self):
        """
        Returns the longest and shortest possible chains.

        """

        file_residues_paths = sorted(glob.glob(os.path.join(self.residue_path, '*.npy')))
        max_res_list_h = []
        max_res_list_l = []

        for f in file_residues_paths:
            idx = self.selected_entries.index(f[-8:-4])
            current_list_h = np.load(f)[1:self.heavy[idx]+1]
            current_list_l = np.load(f)[self.heavy[idx]+1:self.heavy[idx]+self.light[idx]+1]
            current_list_h = [x[1:] for x in current_list_h]
            current_list_l = [x[1:] for x in current_list_l]
            max_res_list_h += list(set(current_list_h).difference(max_res_list_h))
            max_res_list_l += list(set(current_list_l).difference(max_res_list_l))
            
        max_res_list_h = sorted(max_res_list_h, key=noABC)
        min_res_list_h = list(dict.fromkeys([x for x in max_res_list_h]))
        max_res_list_h = [x.strip() for x in max_res_list_h]

        max_res_list_l = sorted(max_res_list_l, key=noABC)
        min_res_list_l = list(dict.fromkeys([x for x in max_res_list_l]))
        max_res_list_l = [x.strip() for x in max_res_list_l]

        for f in file_residues_paths:
            idx = self.selected_entries.index(f[-8:-4])
            current_list_h = np.load(f)[1:self.heavy[idx]+1]
            current_list_l = np.load(f)[self.heavy[idx]+1:self.heavy[idx]+self.light[idx]+1]
            current_list_h = [x[1:] for x in current_list_h]
            current_list_l = [x[1:] for x in current_list_l]
            min_res_list_h = sorted(list(set(current_list_h).intersection(min_res_list_h)))
            min_res_list_l = sorted(list(set(current_list_l).intersection(min_res_list_l)))

        min_res_list_h = [x.strip() for x in min_res_list_h]
        min_res_list_l = [x.strip() for x in min_res_list_l]

        return max_res_list_h, max_res_list_l, min_res_list_h, min_res_list_l


    def initialisation(self, renew_maps, renew_residues):
        """
        Computes the normal mode correlation maps and retrieves lists with the lenghts of the heavy and light chains.

        :return: one list for heavy chains, another for light chains and the selected entries

        """

        dccm_paths = sorted(glob.glob(os.path.join(self.dccm_map_path, '*.npy')))
        selected_entries = [dccm_paths[i][-8:-4] for i in range(len(dccm_paths))]

        if renew_maps:
            self.generate_maps()
        if renew_residues:
            self.get_lists_of_lenghts(selected_entries)

        heavy = np.load(self.chain_lenghts_path+'heavy_lengths.npy').astype(int)
        light = np.load(self.chain_lenghts_path+'light_lengths.npy').astype(int)

        assert list(np.load(self.chain_lenghts_path+'selected_entries.npy')) == selected_entries

        for entry in selected_entries:
            assert len(np.load(self.residues_path+entry+'.npy'))-2 == heavy[selected_entries.index(entry)] + light[selected_entries.index(entry)]

        return heavy, light, selected_entries

    def generate_masked_image(self, img, idx, mode='fully-extended', test_h=None, test_l=None):
        """
        Generates a masked normal mode correlation map

        :param img: original array containing no blank pixels
        :param idx: input index
        :type idx: int
        :param mode: choose between ``fully-cropped`` and ``fully-extended``
        :type mode: str
        :param test_h: length of the heavy chain of an antibody in the test set
        :type test_h: int
        :param test_l: length of the light chain of an antibody in the test set
        :type test_l: int

        :return: masked normal mode correlation map and the mask itself
        
        """       
        f = self.residues_path[idx]
        f_res = np.load(f)
        res_ending = '_residues.npy'
        max_res_h = len(self.max_res_list_h)
        max_res_l = len(self.max_res_list_l)
        max_res = max_res_h + max_res_l 
        masked = np.zeros((max_res, max_res))
        mask = np.zeros((max_res, max_res))
        
        if f.endswith(res_ending):
            f = f.replace(res_ending, '.npy')
            h = test_h
            l = test_l
        else:
            current_idx = self.selected_entries.index(f[-8:-4])
            h = self.heavy[current_idx]
            l = self.light[current_idx]
            

        current_list_h = f_res[1:h+1]
        current_list_h = [x[1:].strip() for x in current_list_h]
        current_list_l = f_res[h+1:h+l+1]
        current_list_l = [x[1:].strip() for x in current_list_l]    
        
        if mode == 'fully-cropped':
            idx_list = [i for i in range(len(current_list_h)) if current_list_h[i] in self.min_res_list_h]
            idx_list += [i+len(current_list_h) for i in range(len(current_list_l)) if current_list_l[i] in self.min_res_list_l]

            masked = img[idx_list,:][:,idx_list] 
            
        
        elif mode == 'fully-extended':
            idx_list = [i for i in range(max_res_h) if self.max_res_list_h[i] in current_list_h]
            idx_list += [i+max_res_h for i in range(max_res_l) if self.max_res_list_l[i] in current_list_l]
            for k, i in enumerate(idx_list):
                for l, j in enumerate(idx_list):
                    #if i in range(120) and j in range(120,215) or i in range(120,215) and j in range(120):
                    #    masked[i, j] = 0
                    #else:    
                    masked[i, j] = img[k, l]
                    mask[i, j] = 1

        else:
            raise NotImplementedError('Unknown mode: choose between fully-cropped and fully-extended')
            
        return masked, mask

    def load_training_images(self, mode='fully_extended'):
        """
        Returns the input/output pairs of the model and their corresponding labels.

        :param mode: choose between ``fully-cropped`` and ``fully-extended``
        :type mode: str
        
        """      
        imgs = []
        kds = []
        labels = []
        file_paths = sorted(glob.glob(os.path.join(self.dccm_map_path, '*.npy')))

        for f in file_paths:
            pdb_id = f[-8:-4]
            if pdb_id in self.selected_entries:
                idx = self.entries.index(pdb_id)
                idx_new = self.selected_entries.index(pdb_id)
                labels.append(pdb_id)
                imgs.append(self.generate_masked_image(np.load(f), idx_new, mode)[0])
                kds.append(np.log10(np.float32(self.affinity[idx])))

        assert labels == self.selected_entries

        for pdb in self.selected_entries:
            assert np.float16(10**kds[self.selected_entries.index(pdb)] == np.float16(self.df[self.df['pdb']==pdb]['affinity'])).all()

        return np.array(imgs), np.array(kds), labels