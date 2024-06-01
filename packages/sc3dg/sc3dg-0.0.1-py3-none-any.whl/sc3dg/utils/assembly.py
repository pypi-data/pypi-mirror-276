import argparse
import re
import numpy as np
import subprocess
import time
import os
import logging
from .scaffold import *
import pandas as pd

def assembly(type_,opt, fastq,log_out):

    print('********run %s || %s*********' % (type_, fastq))
    # 移动到工作目录
    os.chdir(opt['output'])
    # print(opt)
    start = time.time()
 

    # 创建文件夹tmp,并移动
    os.makedirs(opt['type'] + '_' + fastq + '_tmp', exist_ok=True)
    os.chdir(opt['type'] + '_' + fastq + '_tmp')
    os.makedirs('./Result/mcool_folder', exist_ok=True)
    os.makedirs('./Result/cool_folder', exist_ok=True)
    os.makedirs('./Result/SCpair', exist_ok=True)

    
    # 创建logging文件
    logging.basicConfig(filename=fastq + '_logging.log', level=logging.DEBUG)
    for k in opt.keys():

     
        if (k == 'fastq_dir') or (k == 'fastq_log') or (k == 'run_sample'):
            continue
        else:
            logging.debug('# ' + k + ': ' + str(opt[k]))
        
    if os.path.exists(opt['output'] + '/' + opt['type'] + '_' + fastq + '_tmp/Result/' + fastq +'.mcool'):
        log_out.info('The result of ' + fastq + ' has been generated')
        print('==========generated+++++++')
        return
    if os.path.exists(opt['output'] + '/' + opt['type'] + '_' + fastq + '_tmp/Result/SCpair'):
        for val in os.listdir(opt['output'] + '/' + opt['type'] + '_' + fastq + '_tmp/Result/mcool_folder'):
            if val.endswith('.mcool'):
                print('==========generated+++++++')
                return

    
    
    


    fq_r1 = opt['fastq_dir'][opt['fastq_log'].index(fastq)]
    
    fq_r2 = fq_r1.replace('_1.fastq', '_2.fastq')
    
    if type_ == 'scHic' and opt['exist_barcode']:
        
        fq_r3 = fq_r1.replace('_1.fastq', '_3.fastq')
   
        fq_r4 = fq_r1.replace('_1.fastq', '_4.fastq')
   
        if not os.path.exists(fq_r3) or not os.path.exists(fq_r4):
            print(fastq , fq_r3, fq_r4)
            print('The barcode fastq file is not exist')
            log_out.error('The barcode fastq file is not exist')
            return
    
    threads = opt['thread']

    
    if not os.path.exists('Result'):
        os.makedirs('Result')

    # 默认inner和outer barcode和fastq文件放在一个目录下面
    if type_ == 'sciHic':
        opt['inner-barcode'] = os.path.dirname(opt['fastq_dir'][opt['fastq_log'].index(fastq)]) + '/' + fastq + '_inner_barcodes.txt'
        opt['outer-barcode'] = os.path.dirname(opt['fastq_dir'][opt['fastq_log'].index(fastq)]) + '/' + fastq + '_outer_barcodes.txt'



    # fastp,获得trimmed-pair1/2.fastq.gz,传入后续比对
    if opt['exist_barcode']:
        if type_ == 'snHic':
            t = fastp(fq_r1, fq_r2, 
                      'trimmed-pair1.fastq.gz', 'trimmed-pair2.fastq.gz',
                      threads, max=False)
            snHic_barcode('trimmed-pair1.fastq.gz', 'trimmed-pair2.fastq.gz')


        if type_ == 'scHic':
            print('making index..............')
            t  = GetFastqIndex(fastq, fq_r1, fq_r4, fq_r2, fq_r3)
            logging.info('make_index::: %s '%t)

            t = fastp('%s._1_barcode.fastq.gz'%fastq,
                    '%s._2_barcode.fastq.gz'%fastq, 
                    'trimmed-pair1.fastq.gz', 
                    'trimmed-pair2.fastq.gz',threads,  max=True)
            logging.info('fastp::: %s '%t)

        if type_ == 'sciHic':
            t = fastp(fq_r1,
                      fq_r2,
                      'trimmed-pair1_before.fastq.gz',
                        'trimmed-pair2_before.fastq.gz',
                        threads, max=False,
                        adapter=['AGATCGGAAGAGCGATCGG', 'AGATCGGAAGAGCGTCGTG']
                      )
            logging.info('fastp::: %s '%t)

            t = time.time()
            inline_splitter('trimmed-pair1_before.fastq.gz', 
                            'trimmed-pair2_before.fastq.gz',
                            opt['outer-barcode'], 
                            'trimmed-pair1_before2.fastq.gz', 
                            'trimmed-pair2_before2.fastq.gz',
                            fastq + '.splitting_stats.html')
            logging.info('inline_splitter::: %s '% (time.time()- t))

            t = time.time()
            analyze_scDHC_V2design(opt['inner-barcode'],
                            'trimmed-pair1_before2.fastq.gz', 
                            'trimmed-pair2_before2.fastq.gz',
                            'trimmed-pair1.fastq.gz', 
                            'trimmed-pair2.fastq.gz'
                            )
            logging.info('analyze_scDHC_V2design::: %s ' % (time.time()- t))

            t = time.time()
            awk()
            logging.info('awk::: %s ' % (time.time()- t))

    else:
        t = fastp(fq_r1, fq_r2, 'trimmed-pair1.fastq.gz', 'trimmed-pair2.fastq.gz',threads, max=False)
        logging.info('fastp::: %s '%t)
    

    # bwa,获得sam文件
    if opt['aligner'] == 'bwa':
        t = bwa(opt['index'], threads,fastq)
        logging.info('bwa::: %s '%t)
    else:
        t = bowtie2(opt['index'], threads,fastq)
        logging.info('bowtie2::: %s '%t)

    # # 比对的sam转bam
    t = sam_to_bam(fastq, threads)
    logging.info('sam_to_bam::: %s '%t)

    # # 质控bam文件
    t = samtools_qc(threads, opt['qc'], fastq)
    logging.info('samtools_qc::: %s '%t)

    # pairtools parse
    t = pairtools_parse(fastq, 
                        opt['genomesize'],
                        opt['species'],
                         opt['add_columns'],
                         threads
                        )
    logging.info('pairtools_parse::: %s '%t)


    # # pairtools restrict
    t = pairtools_restrict(fastq,opt['enzyme_bed'])
    logging.info('pairtools_restrict::: %s '%t)

    # # pairtools select
    t = pairtools_select(fastq, opt['select'])
    logging.info('pairtools_select::: %s '%t)

    # # pairtools sort 
    t = pairtools_sort(fastq)
    logging.info('pairtools_sort::: %s '%t)

    # pairtools dedup
    t = pairtools_dedup(fastq,str(opt['max_mismatch']))
    logging.info('pairtools_dedup::: %s '%t)

    

    if opt['exist_barcode']:
        split_cells(fastq)
        t = time.time()
        for p in os.listdir('./Result/SCpair'):
            if p.endswith('pairs.gz'):
       
                cload_correct_zoomify('./Result/SCpair/',
                                      p,
                                      opt['genomesize'],
                                      str(opt['resolution']),
                                       opt['zoomify_res']
                                      )
        logging.info('sub_cload_correct_zoomify::: %s '% (time.time() - t))
    else:
        # 整体的mcool
        t = cooler_cload_pairs(opt['genomesize'],
                                str(opt['resolution']),
                                fastq
                                ,prefix='dedup'
                                )
        logging.info('cooler_cload_pairs::: %s '%t)

        t = KR_correctMatrix(fastq,str(opt['resolution']) )
        logging.info('KR_correctMatrix::: %s '%t)

        t = cooelr_zoomify(fastq,opt['resolution'], opt['zoomify_res'])
        logging.info('cooelr_zoomify::: %s '%t)
 
    os.system('mv ./*.mcool ./Result/mcool_folder/')
    os.system('mv ./*.cool ./Result/cool_folder/')
    os.system('mv ./*restrict.pairs.gz ./Result/SCpair/')
    os.system('mv ./%s.pairs.gz ./Result/SCpair/'%fastq)
    os.system('mv ./Result/SCpair/*.mcool ./Result/mcool_folder')
    os.system('mv ./Result/SCpair/*.cool ./Result/cool_folder')
    for val in os.listdir('./'):
        if not os.path.isdir(val):
            if val == fastq + '_logging.log' or val == fastq + '.bam' or val == fastq + '.qc.bam' or val == fastq + '.merged.bam' or val =='trimmed.fastp.json':
                continue
            else:
                print(val)
                os.remove(val)


    
    logging.info('total time: %s' % (time.time() - start))
    









    
    

    

        
        

    