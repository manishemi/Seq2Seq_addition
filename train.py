from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import numpy as np

symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '+']


def genarate(symbols, max_number, max_sample, max_random_data_length):
    return Data_generation(symbols, max_number, max_sample
                           , max_random_data_length).process()


def return_format():
    return Data_generation.Random_data


def test_preprocess(x, symbols):
    int_data = dict((i, j) for i, j in enumerate(symbols))
    temp = []
    for value in x:
        string = int_data[np.argmax(value)]
        temp.append(string)
    return ''.join(temp)


class Data_generation():
    Random_data = []

    def __init__(self, symbols, max_number, max_sample, max_random_data_length):
        self.symbols = symbols
        self.max_number = max_number
        self.max_sample = max_sample
        self.max_random_data_length = max_random_data_length

    def random_generate(self):
        random_labels = []
        random_data = []
        for _ in range(max_sample):
            num1 = np.random.randint(1, max_number)
            num2 = np.random.randint(1, max_number)
            sum = str(num1 + num2)
            if len(sum) < len(str(max_number)):
                sum += ''.join(' ' for _ in range(len(str(max_number)) - len(sum)))
            data_gen = str(num1) + "+" + str(num2)
            if len(data_gen) < max_random_data_length:
                data_gen += ''.join(' ' for _ in range(max_random_data_length - len(data_gen)))
            random_data.append(data_gen)
            random_labels.append(sum)
        Data_generation.Random_data = random_data
        return random_data, random_labels

    def encode(self, x, y):
        encoded_data = []
        encoded_labels = []
        for operations in x:
            int_data = [symbols.index(value) for value in operations]
            encoded_data.append(int_data)
        for number in y:
            int_label = [symbols.index(value) for value in number]
            encoded_labels.append(int_label)

        return encoded_data, encoded_labels

    def one_hot(self, x, y):
        one_hot_label = []
        one_hot_data = []
        for value in x:
            temp = []
            for i, j in enumerate(value):
                zeros = np.zeros(len(self.symbols))
                zeros[j] = 1
                temp.append(zeros)
            one_hot_data.append(temp)

        for value in y:
            temp = []
            for i, j in enumerate(value):
                zeros = np.zeros(len(self.symbols))
                zeros[j] = 1.
                temp.append(zeros)
            one_hot_label.append(temp)

        x = np.array(one_hot_data)
        y = np.array(one_hot_label)
        return x, y

    def process(self):
        x, y = self.random_generate()
        x, y = self.encode(x, y)
        x, y = self.one_hot(x, y)
        return x, y

    def data_format(self):
        x, y = self.random_generate()
        return x, y


max_number = 100
max_sample = 10000
max_random_data_length = len(str(max_number) + "+" + str(max_number))
n_times_repeatvector = int(np.log10(max_number) + 1)
model = Sequential()
model.add(layers.LSTM(100, input_shape=(max_random_data_length, len(symbols))))
model.add(layers.RepeatVector(n_times_repeatvector))
model.add(layers.LSTM(50, return_sequences=True))
model.add(layers.TimeDistributed(layers.Dense(len(symbols), activation='softmax')))

model.compile(
    loss="categorical_crossentropy",
    optimizer="adam",
    metrics=["acc"]
)

epochs = 80
batch_size = 100
for i in range(epochs):
    x, y = genarate(symbols, max_number, max_sample, max_random_data_length)
    model.fit(
        x,
        y,
        epochs=1,
        batch_size=batch_size
    )

x, y = genarate(symbols, max_number, max_sample, max_random_data_length)
test_format = return_format()
result = model.predict(x, batch_size=batch_size, verbose=0)
predict = [test_preprocess(x, symbols) for x in result]

for i in range(15):
    print("{}= {}".format(test_format[i], predict[i]))
