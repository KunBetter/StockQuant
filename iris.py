from sklearn import datasets
from sklearn import tree
from sklearn.model_selection import train_test_split

data = datasets.load_iris()['data']
target = datasets.load_iris()['target']
# 导入数据，data是鸢尾花的花萼宽度长度、花瓣长度宽度，target是该鸢尾花的品种，有0,1,2三种类型

trainx, testx, trainy, testy = train_test_split(data, target, test_size=0.2)
# 造一个大象，将源数据拆分成训练集和测试集，测试集是总数据的20%

clf = tree.DecisionTreeClassifier()
# 创建一个名为clf的冰箱，创建一个模型，参数全部用默认

clf.fit(trainx, trainy)
# 把大象塞进冰箱，训练这个模型

print('预测值：', clf.predict(testx))
# 看看训练完的冰箱的工作能力

print('实际值：', testy)
# 看看实际的值

print('预测准确率：%2.2f%%' % (clf.score(testx, testy) * 100))
