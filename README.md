# DoubleArrayTrie
双端trie树的python实现

版本翻译于https://github.com/digitalstain/DoubleArrayTrie.git的Java实现，
将其改写成python3.5版本

最主要的贡献是 —— 1：实现了其模糊查询的功能；2：自定义编码值，解决双端trie树需要预定义字母表的问题

另外，有实现了字典Trie树，字典Trie树构建简单、模糊查找功能实现容易，无需状态记录；其与双数组Tire可以说在功能上互补；
在存储值很多且多有冲突、字符编码范围较大的情况下，双数组Trie树很可能在序列化到硬盘以及加载到内存的占用空间都远大于字典Trie树