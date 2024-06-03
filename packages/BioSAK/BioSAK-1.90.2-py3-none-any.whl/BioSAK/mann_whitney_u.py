import argparse
from scipy.stats import mannwhitneyu


mannwhitneyu_usage = '''
============== mannwhitneyu example commands ============== 

BioSAK mannwhitneyu -i genome_size_by_lifestyle.txt

# file format: no header, tab separated.
1.61	nonsponge
1.59	nonsponge
1.47	sponge
1.52	sponge

===========================================================
'''


def mann_whitney_u(args):

    file_in = args['i']

    value_dict = dict()
    for each_s in open(file_in):
        each_s_split = each_s.strip().split('\t')
        s_cate  = each_s_split[1]
        s_value = float(each_s_split[0])
        if s_cate not in value_dict:
            value_dict[s_cate] = [s_value]
        else:
            value_dict[s_cate].append(s_value)

    if len(value_dict) != 2:
        cate_list = sorted(list(value_dict.keys()))
        print('Group number has to be 2, program exited!')
        print('Currently has: %s' % ','.join(cate_list))
        exit()

    value_lol = [value_dict[i] for i in value_dict]
    _, p_value = mannwhitneyu(value_lol[0], value_lol[1])

    print('P value: %s' % p_value)


if __name__ == '__main__':

    mannwhitneyu_parser = argparse.ArgumentParser()
    mannwhitneyu_parser.add_argument('-i', required=True, help='input file')
    args = vars(mannwhitneyu_parser.parse_args())
    mann_whitney_u(args)
