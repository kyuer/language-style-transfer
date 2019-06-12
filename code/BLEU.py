# -*- coding: utf-8 -*-
# @Time    : 2019-05-29 16:23
# @Author  : MarsDidi
# @Email   : xiatianci_i@didiglobal.com
# @File    : BLEU.py.py

from nltk.translate.bleu_score import sentence_bleu


reference = [['The', 'cat', 'is', 'on', 'the', 'mat']]
candidate = ['The', 'cat', 'sat', 'on', 'the', 'mat']
score = sentence_bleu(reference, candidate)
print(score)

# -*- coding:utf-8 -*-
"""
Description:
    1) 使用nltk包中的bleu计算工具来进行辅助计算
"""
import numpy as np
import re
from nltk.translate.bleu_score import corpus_bleu

def my_bleu_v1(candidate_token, reference_token):
    """
    :param candidate_set:
    :param reference_set:
    :description:
    最简单的计算方法是看candidate_sentence 中有多少单词出现在参考翻译中, 重复的也需要计算. 计算出的数量作为分子
    分母是候选句子中的单词数量
    :return: 候选句子单词在参考句子中出现的次数/候选句子单词数量
    """
    # 分母是候选句子中单词在参考句子中出现的次数 重复出现也要计算进去
    count = 0
    for token in candidate_token:
        if token in reference_token:
            count += 1
    a = count
    # 计算候选翻译的句子中单词的数量
    b = len(candidate_token)
    return a/b


def calculate_average(precisions, weights):
    """Calculate the geometric weighted mean."""
    tmp_res = 1
    for id, item in enumerate(precisions):
        tmp_res = tmp_res*np.power(item, weights[id])
    tmp_res = np.power(tmp_res, np.sum(weights))
    return tmp_res


def calculate_candidate(gram_list, candidate):
    """Calculate the count of gram_list in candidate."""
    gram_sub_str = ' '.join(gram_list)
    return len(re.findall(gram_sub_str, candidate))


def calculate_reference(gram_list, references):
    """Calculate the count of gram_list in references"""
    gram_sub_str = ' '.join(gram_list)
    gram_count = []
    for item in references:
        # calculate the count of the sub string
        gram_count.append(len(re.findall(gram_sub_str, item)))
    return gram_count


def my_bleu_v2(candidate_sentence, reference_sentences, max_gram, weights,mode=0):
    """
    :param candidate_sentence:
    :param reference_sentence:
    :description: 上诉的最初版本的bleu指标存在比较大的缺陷 如常用词语(the on) 等 由于出现的频率比较高
    会导致翻译结果比较差的时候也能够得到较高的bleu值
    改进行的bleu方法中使用到了n-grams precision方式更改分母的计算法则 使得不是简单的计算单个词汇出现次数
    原有的初始方法是一一个词为基准计算分母 现在改进方法采用n 个词作为一个组用于计算分母 其中n可以从1取到最大
    这样如果事先决定了所要计算gram的最大长度(N) 那么可以在candidate sentence 和 reference sentences 上计算出每一个
    长度的gram 的精度 然后对精度进行几何加权平均即可
    :return:
    """
    candidate_corpus = list(candidate_sentence.split(' '))
    # number of the reference sentences
    refer_len = len(reference_sentences)
    candidate_tokens_len = len(candidate_corpus)
    # 首先需要计算各种长度的gram 的precision值
    if mode == 0:
        # method1 to calculate the bleu
        # 计算当前gram 在candiate_sentence中出现的次数 同时计算这个gram 在所有的reference sentence中的出现的次数
        # 每一次计算时将当前candidate_sentence中当前gram出现次数与在当前reference sentence中出现的gram次数选择最小值
        # 作为这个gram相对于 参考文献j的截断次数
        # 然后将所有的参考文献对应的截断次数做最大值 作为这个gram在整个参考文献上的综合截断值 这个值就是当前gram对应的分子
        # 分母依然是这个gram 在candidate sentence中出现的次数
        # 在计算当前长度(n)的其他的gram的综合截断次数 然后加起来作为长度为n的gram的综合截断次数值 分母是所有长度为n的gram的相加的值
        # 两个值相除即可得到这个长度为n的gram 的precision值
        # procedure
        gram_precisions= []
        for i in range(max_gram):
            # calculate each gram precision
            # set current gram length
            curr_gram_len = i+1
            # calculate current gram length mole(分子)
            curr_gram_mole = 0
            # calculate current gram length deno(分母)
            curr_gram_deno = 0
            for j in range(0, candidate_tokens_len, curr_gram_len):
                if j + curr_gram_len > candidate_tokens_len:
                    continue
                else:
                    curr_gram_list = candidate_corpus[j:j+curr_gram_len]
                    gram_candidate_count = calculate_candidate(curr_gram_list, candidate_sentence)
                    # print(' current gram candidate count')
                    # print(gram_candidate_count)
                    gram_reference_count_list = calculate_reference(curr_gram_list, reference_sentences)
                    # print(' current gram reference count list')
                    # print(gram_reference_count_list)
                    truncation_list = []
                    for item in gram_reference_count_list:
                        truncation_list.append(np.min([gram_candidate_count, item]))
                    curr_gram_mole += np.max(truncation_list)
                    curr_gram_deno += gram_candidate_count
            print(' current length %d and gram mole %d and deno %d' % (i+1, curr_gram_mole, curr_gram_deno))
            gram_precisions.append(curr_gram_mole/curr_gram_deno)
        print('all the precisions about the grams')
        print(gram_precisions)

        # method2 to calculate the bleu
        # 第二种计算方法与第一种计算方法本质上的区别在于计算截断计数的区别(最终结果是一样的)
        # 先计算当前n长度的gram在所有的参考文献中的出现次数的最大值 然后在与当前gram在candidate sentence中出现的次数的最小值
        # 作为综合截断计数 本质上讲两种方法得到的结果是一样的 不在缀述

    # 其次对多元组合(n-gram)的precision 进行加权取平均作为最终的bleu评估指标
    # 一般选择的做法是计算几何加权平均 exp(sum(w*logP))
        average_res = calculate_average(gram_precisions, weights)
        print(' current average result')
        print(average_res)
    # 最后引入短句惩罚项 避免短句翻译结果取得较高的bleu值, 影响到整体评估
    # 涉及到最佳的匹配长度 当翻译的句子的词数量与任意的参考翻译句子词数量一样的时候 此时无需惩罚项
    # 如果不相等 那么需要设置一个参考长度r 当翻译的句子长度(c) 大于 r 的时候不需要进行惩罚 而 当c小于r
    # 需要在加权平均值前乘以一个惩罚项exp(1-r/c) 作为最后的bleu 指标输出
    # r 的选择可以这样确定 当翻译句子长度等于任何一个参考句子长度时不进行惩罚 但是当都不等于参考句子长度时
    # 可以选择参考句子中最长的句子作为r 当翻译句子比r 长时不进行惩罚 小于r时进行惩罚
    bp = 1
    reference_len_list = [len(item.split(' ')) for item in reference_sentences]
    if candidate_tokens_len in reference_len_list:
        bp = 1
    else:
        if candidate_tokens_len < np.max(reference_len_list):
            bp = np.exp(1-(np.max(reference_len_list)/candidate_tokens_len))
    return bp*average_res


if __name__ == '__main__':
    candidate_sentence = 'hello this is my code'
    reference_sentence = 'hello this code is not mine'
    candidate_token = candidate_sentence.split(' ')
    reference_token = reference_sentence.split(' ')
    bleu_v1_score = my_bleu_v1(candidate_token, reference_token)
    print('bleu version 1 score is %.2f ' % bleu_v1_score)


    # full bleu test on references and candidate
    predict_sentence = 'how old is the man'
    train_sentences = ['this is a dog and not is a cat', 'this is a cat and not is a dog', 'it is a dragon', 'i like play ball']
    bleu_v2_score = my_bleu_v2(predict_sentence, train_sentences, 4, weights=[0.25, 0.25, 0.25, 0.25], mode=0)