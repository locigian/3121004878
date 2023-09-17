from line_profiler import LineProfiler

lp = LineProfiler()

@lp
def your_function_to_profile():
    import jieba
    import re
    import gensim
    import sys

    def preprocess_text(text):
        # 使用jieba进行分词，并过滤掉非中文字符
        words = jieba.lcut(text)
        chinese_words = [word for word in words if re.match(u"[\u4e00-\u9fa5]", word)]
        return chinese_words

    def calculate_similarity(text1, text2):
        texts = [text1, text2]
        # 创建词典
        dictionary = gensim.corpora.Dictionary(texts)
        # 创建文档向量
        corpus = [dictionary.doc2bow(text) for text in texts]
        # 计算相似度
        similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
        test_corpus = dictionary.doc2bow(text1)
        cosine_similarity = similarity[test_corpus][1]
        return cosine_similarity * 100  # 转换为百分比形式

    def main():
        if len(sys.argv) != 4:
            print("用法: main.py <原文文件> <抄袭版论文的文件> <答案文件>")
            sys.exit(1)

        original_file_path = sys.argv[1]  # 原文文件路径
        copied_file_path = sys.argv[2]  # 抄袭版文件路径
        answer_file_path = sys.argv[3]  # 答案文件路径

        try:
            with open(original_file_path, 'r', encoding='utf-8') as original_file, \
                    open(copied_file_path, 'r', encoding='utf-8') as copied_file:
                original_text = original_file.read()  # 读取原文内容
                copied_text = copied_file.read()  # 读取抄袭版文本内容

                text1 = preprocess_text(original_text)  # 预处理原文
                text2 = preprocess_text(copied_text)  # 预处理抄袭版文本
                similarity = calculate_similarity(text1, text2)  # 计算相似度

                with open(answer_file_path, 'w', encoding='utf-8') as answer_file:
                    answer_file.write(f"文章重复率为：{similarity:.2f}%")
                    print(f"文章重复率为：{similarity:.2f}%")

        except FileNotFoundError:
            print("文件不存在")
            sys.exit(1)

    if __name__ == "__main__":
        main()


if __name__ == "__main__":
    your_function_to_profile()
    lp.print_stats()
