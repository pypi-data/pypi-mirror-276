import pandas as pd 
import json, argparse, os
import numpy as np  

SCICLONE_COLUMNS = ["chr", "start", "refCount", "varCount", "VAF"]

def sciclone_fmt(output_path, ssm_fn, params_fn, name_converison_fn):
    """
    Processes ssm dataframe into a tsv that can be used by SciClone
    """
    name_conversion_df = None
    if name_converison_fn != None:
        name_conversion_df = pd.read_csv(name_converison_fn)
    dataframe = pd.read_csv(ssm_fn, sep="\t")

    params = json.load(open(params_fn))
    samples = params["samples"]
    clusters = params["clusters"]
    ssms = [c[0] for c in clusters]

    vaf_data = {s:[] for s in samples}
    copy_num_data = {s:[] for s in samples}

    for vid in ssms:

        row = dataframe[dataframe["id"] == vid].iloc[0]

        name = row["name"]

        # iterate through all var_read, ref_reads, var_read_prob per row
        for var_reads, total_reads, var_read_prob, sample in zip([int(cnt) for cnt in row["var_reads"].split(",")],
                                                               [int(cnt) for cnt in row["total_reads"].split(",")],
                                                               [float(prob) for prob in row["var_read_prob"].split(",")],
                                                               samples):
            segment_mean = 0
            if isinstance(name_conversion_df, pd.DataFrame):
                chr = name_conversion_df.loc[name_conversion_df["Gene"] == name, "chr"].values[0]
                if (chr != "X") and (chr != "Y"):
                  chr = int(chr)
                else:
                  segment_mean = -1
                pos = name_conversion_df.loc[name_conversion_df["Gene"] == name, "pos"].values[0]
            else:
                chr, pos = name.split("_")
                if (chr != "X") and (chr != "Y"):
                  chr = int(chr)
                else:
                  segment_mean = -1
                pos = int(pos)
            total_reads_diploid = int(2*total_reads*var_read_prob)
            var_reads_diploid = np.minimum(int(var_reads), total_reads_diploid)
            
            # assume everything is either diploid or haploid and in a non-CNA effected region

            vaf_data[sample].append([chr, pos, total_reads_diploid-var_reads_diploid, var_reads_diploid, 100*var_reads_diploid/np.maximum(1, int(total_reads_diploid))])
            copy_num_data[sample].append([chr, pos, pos, segment_mean])
    for sample in samples:
      os.mkdir(os.path.join(output_path, sample))
      pd.DataFrame(vaf_data[sample], columns=SCICLONE_COLUMNS).to_csv(os.path.join(output_path, sample, sample + ".vaf.tsv"), sep="\t", index=False)
      pd.DataFrame(copy_num_data[sample]).to_csv(os.path.join(output_path, sample, sample + ".cn.tsv"), sep="\t", header=False, index=False)

def _parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(

        description="convert ssm file to be used by pyclone-vi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter

    )

    parser.add_argument('output_path', help='Output path to write all sample files')
    parser.add_argument('ssm_fn', help='Simple somatic mutation file.')
    parser.add_argument('params_fn', help='Parameters file')
    parser.add_argument('-c', '--name-conversion-fn', help='File for containing info for converting name to chr, pos.', default=None)



    args = parser.parse_args()

    return args


def main():
    """
    Converts ssm file to file that can be read by SciClone
    """
    args = _parse_args()

    sciclone_fmt(args.output_path, args.ssm_fn, args.params_fn, args.name_conversion_fn)


if __name__ == '__main__':
  main()
