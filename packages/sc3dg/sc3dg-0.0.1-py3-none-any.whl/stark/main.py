import argparse
import os
from utils import scSPRITE,sn_m3c,scNano,scMethyl
from utils import help
from utils import tools as tl
import time
from multiprocessing import Process, Queue, Pool, Manager
from utils.scaffold import *
from utils.assembly import *
import logging
Path = os.getcwd()
print(Path)
tech = {
        'scSPRITE':scSPRITE,
        
        'sn_m3c':sn_m3c,
        'scNano':scNano,
        'scMethyl': scMethyl
       }

def run_pipeline(opt):
    # 转化为字典
    opt = dict(opt.__dict__)
    opt['running_path'] = Path

    # 先创建output文件夹，没有则创建，有则退出;然后移到该工作目录下面
    tl.make_workflow(opt['output'])
    os.chdir(opt['output'])

    # 然后判断是不是到底有多少个样本，如果是一个样本，那么就直接运行，如果是多个样本，那么就要用多进程来运行
    opt, fastq_log = tl.count_sample(opt)

 

    # 判断index是否存在
    tl.check_index(opt)
    tl.check_enzyme(opt)

    tl.get_enzyme_bed(opt)

    opt = tl.parser_fa_and_chrom_size(opt)

    # 查询是什么物种
    opt['species'] = tl.parse_species(opt)
    
    # print(opt)
    
    
    # gobal logging
    log_out = tl.log_(opt)
    os.chdir(opt['output'])

    if len(fastq_log) <= opt['worker']:
        print('*****num of worker is more than num of sample*****')
        p = Pool(opt['worker'])
        for fq in fastq_log:
            # 根据type来允许不同的流程
           run_exec(opt['type'],opt, fq,log_out)
        p.close()
        p.join()
    else:
        print('*****num of worker is less than num of sample*****')
        divide_list = []
        for i in range(0, len(fastq_log), opt['worker']):
            divide_list.append(fastq_log[i:i + opt['worker']])

        # logging batch 
        log_out.debug('divide_list:{}'.format(len(divide_list)))

        for i,val in enumerate(divide_list):
            p = Pool(len(val))
            for j,fq in enumerate(val):
                log_out.debug('%s || %s.....Dealing fq: %s \n' % (i*opt['worker']+ j,len(fastq_log),fq))
               
            
                p.apply_async(run_exec, args=(opt['type'],opt, fq,log_out))
                
            p.close()
            p.join()
            log_out.debug('Batch %s done || %s \n' % (i,len(divide_list)/opt['worker']))
    log_out.debug('All done || %s \n' % (len(fastq_log)))

def run_exec(type_,opt, fq,log_out):
    print(type_)
    if type_ == 'sn_m3c' or type_ == 'scSPRITE' or type_ == 'scNano' or type_ == 'scMethyl':
        if (type_ == 'sn_m3c' or type_ == 'scMethyl' )and opt['aligner'] == 'bwa':
            log_out.debug('sn_m3c only support bowtie2')
            print('sn_m3c only support bowtie2')
            return
        print(type_)
        exec(type_ + '.pp' + '(opt=opt,fastq=fq,log_out=log_out)')
    else:
        assembly(type_,opt, fq,log_out)

    






def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--output', help='save path',required=True,
                        default=None)
    parser.add_argument('-f', '--fastq', required=True,
                        default=None, 
                        help='fastq_dir, run all if -s is not be specfied',)
    parser.add_argument('--logging', help='logging', default='./log.log')
    parser.add_argument('-t', '--type',required=True,
                        choices=['scHic', 'snHic','sciHic','scSPRITE','dipC','sn_m3c','HIRES', 'scNano', 'scMethyl', 'LiMAC','scCARE'],
                         help='type of hic',default=None, )
    parser.add_argument('-e', '--enzyme', help='enzyme,mboi',nargs='+',type=str,required=True,
                        default=None)
    parser.add_argument('-r', '--resolution', help='resoluation', default=10000)
    parser.add_argument('-i', '--index', help='bwa fa file/bowtie fa file',required=True,
                        default=None, )
    parser.add_argument('-s', '--sample', help='sample, txt',
                        default=None)
    parser.add_argument('--exist-barcode' , action='store_true', help='barcode is exist')
    parser.add_argument('--qc', type=int, default=0, help='samtools view to qc')
    parser.add_argument('--add-columns', default='mapq', help=help.help['add_columns'])
    parser.add_argument('--thread', help='thread', type=int, default=20)
    parser.add_argument('--worker', help='simouteously run the worker of the pipeline', type=int, default=2)
    parser.add_argument('--select', help=help.help['select'],default="mapq1>=30 and mapq2>=30")
    parser.add_argument('--max-mismatch', help=help.help['max_mismatch'], type=int, default=3)
    parser.add_argument('--aligner', default='bwa', choices=['bwa', ' bowtie2'], help='aligner')
    parser.add_argument('--repeat-masker', help='repeat masker(bed file) for scSPRITE', default='/cluster/home/Kangwen/common/mm10_rmsk.bed')
    parser.add_argument('--sprite-config', help='sprite-config', default=None)
    parser.add_argument('--scNano-barcode',default=None,
                        help='scNano barcode for PCR and TN5, which should be stored in a folder and named as TN5.txt and PRC,index.txt.txt respectively')
    parser.add_argument('--zoomify-res', help='zoomify',type=str, default='10000,40000,100000,500000,1000000')
    
    args = parser.parse_args()
    run_pipeline(args)


if __name__ == '__main__':
    Time = time.time()
    main()
    print('=============time spen ', time.time() - Time, '===================')