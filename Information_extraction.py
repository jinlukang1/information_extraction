import jieba
import tqdm
from utils import load_txt, get_online_text, write_txt

def seg_words(input_str):
    # 利用jieba对语段进行分词
    seg_list = jieba.cut(input_str, cut_all=False)
    # tags = analyse.extract_tags(input_str, topK=5, withWeight=True)
    return seg_list

def load_dataset(dataset_path):
    # 加载自己写的简单的语料库
    dataset_txt = []
    dataset_list = load_txt(dataset_path)
    for line in dataset_list:
        temp_list = line.split('|')
        for i in temp_list:
            if len(i) >= 2:
                dataset_txt.append(i)
    return dataset_txt

def judge_txt(input_txt, dataset):
    # 查看爬取内容中有多少相关词汇
    count = 0
    try:
        online_txt = get_online_text(input_txt)
    except:
        return -1
    for data in dataset:
        if data in online_txt:
            count += online_txt.count(data)
    return count

def pridict(result_list, topK):
    # 预测最优的K个结果
    for i in range(len(result_list)):
        max_index = i
        for j, (seg_word, result) in enumerate(result_list):
            if int(result_list[max_index][1]) <= int(result) and i < j:
                max_index = j
        result_list[i], result_list[max_index] = result_list[max_index], result_list[i]
    fin_list = result_list[:topK]
    return fin_list

def main():
    txt_path = './data.txt'
    txt_list = load_txt(txt_path)
    data_path = './dataset.txt'
    dataset_txt = load_dataset(data_path)
    fin_result_list = []
    # 对划分的内容逐个处理
    print('{} sentence to do.'.format(len(txt_list)))
    for txt_line in txt_list:
        result_list = []
        seg_list = seg_words(txt_line)
        print('Sentence index : {}.'.format(txt_list.index(txt_line) + 1))
        for seg_word in tqdm.tqdm(list(set(seg_list))):
            if len(seg_word) <= 1:
                continue
            result = judge_txt(seg_word, dataset_txt)
            result_list.append((seg_word, result))
            # print('{} : {}'.format(seg_word, result))
        fin_result_list.extend(result_list)
    write_txt(fin_result_list, './result.txt')
    result_list = load_txt('./result.txt')
    result_list = [result.replace('(', '').replace(')', '').replace(' ', '').split(',') for result in result_list]
    top_list = pridict(result_list, 10)
    print(top_list)


if __name__ == '__main__':
    main()