import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# EOS char => #

class BasicLSTM(nn.Module):
	def __init__(self, num_classes, input_size, hidden_size, num_layers):
		# github copilot suggestion
		super(BasicLSTM, self).__init__()
		self.num_classes = num_classes
		self.num_layers = num_layers
		self.input_size = input_size
		self.hidden_size = hidden_size
		# I figure we will need this one, should be 27 for alpahebet plus EOS
		# self.seq_length = 27
		self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
		# self.fc_1 = nn.Linear(hidden_size, 64)
		# self.fc_2 = nn.Linear(64, num_classes)
		# starting with a smaller number of nodes to keep training time down
		self.fc_1 = nn.Linear(hidden_size, 32)
		self.fc_2 = nn.Linear(32, num_classes)

		# this one wasn't suggested by copilot, not needed? a ReLu can't hurt though..
		self.relu = nn.ReLU()

	def fwd(self, x):
		# h0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))
		# c0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))
		# github copilot suggestion
		# Set initial states
		h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
		c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)

		# Forward propagate LSTM
		# out, _ = self.lstm(x, (h0, c0)) #lstm 
		# do we not need cn? 
		out, (hn, cn) = self.lstm(x, (h0, c0)) #lstm 
		hn = hn.view(-1, self.hidden_size) # Reshape output to (batch_size*sequence_length, hidden_size)
		out = self.relu(hn)
		out = self.fc_1(out)
		out = self.relu(out)
		out = self.fc_2(out)
		return out


def get_names_from_file():
	with open("names.txt") as f:
		lines = f.readlines()
	for idx, val in enumerate(lines):
		lines[idx] = val.lower()
	return lines

# todo generate this programatically so we don't have a huge sparse matrix in source
alphas = {
	'a'	: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'b'	: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'c'	: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'd'	: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'e'	: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'f'	: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'g'	: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'h'	: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'i'	: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'j'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'k'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'l'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'm'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'n'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'o'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'p'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'q'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	'r'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
	's'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
	't'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
	'u'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
	'v'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 
	'w'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
	'x'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
	'y'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
	'z'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
	'#'	: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
}

def name_to_vector_repr(name: str) -> np.array:
	eos_char = np.array(alphas['#'])

	vector_repr = []
	for char in name:
		if char == '\n':
			vector_repr.append(eos_char)
			continue
		vector_repr.append(np.array(alphas[char]))

	if len(vector_repr) < 11:
		for i in range(11 - len(vector_repr)):
			vector_repr.append(eos_char)

	return np.array(vector_repr)

def main():

	names = get_names_from_file()

	names_vector = [name_to_vector_repr(name) for name in names]

	x = names_vector
	length = len(x)
	x_train = x[0:int(0.8*length)]
	x_validate = x[int(0.8*length):length]
	X_train_tensor = [torch.from_numpy(x).float() for x in x_train]
	X_validate_tensor = [torch.from_numpy(x).float() for x in x_validate]

	X_train_tensor = torch.vstack(X_train_tensor)
	X_validate_tensor = torch.vstack(X_validate_tensor)

	# X_train_tensor = torch.reshape(X_train_tensor, (X_train_tensor.shape[0], 1, X_train_tensor.shape[1], X_train_tensor.shape[2]))
	# X_validate_tensor = torch.reshape(X_validate_tensor, (X_validate_tensor.shape[0], 1, X_validate_tensor.shape[1], X_validate_tensor.shape[2]))

	X_train_tensor = torch.reshape(X_train_tensor, (X_train_tensor.shape[0], 1, X_train_tensor.shape[1]))
	X_validate_tensor = torch.reshape(X_validate_tensor, (X_validate_tensor.shape[0], 1, X_validate_tensor.shape[1]))

	num_epochs = 100
	eta = 0.01 # learning rate
	input_size = 27 # 27 letters in the alphabet + # for end of string
	num_classes = 27 # 27 letters in the alphabet + # for end of string
	hidden_size = 27 # number of hidden units in the LSTM cell
	num_layers = 1 # stacked LSTM layers

	ltsm = BasicLSTM(num_classes, input_size, hidden_size, num_layers)	

	criterion = nn.CrossEntropyLoss()
	# criterion = nn.MSELoss()
	optimizer = torch.optim.Adam(ltsm.parameters(), lr=eta)

	epochs_v_loss = []

	# train the model
	for epoch in range(num_epochs):
		outputs = ltsm.fwd(X_train_tensor) # forward pass
		optimizer.zero_grad() # clear gradients

		# is [17602, 1, 27]
		X_train_tensor = X_train_tensor.reshape([X_train_tensor.shape[0], X_train_tensor.shape[2]])
		# now should be [17602, 27]

		# obtain the loss function
		loss = criterion(outputs, X_train_tensor)
		# this should be labels right, but we don't have labels hmmm....
		# loss = criterion(outputs, Y_train_tensor)

		loss.backward() # backward pass

		optimizer.step() # update the parameters
		epochs_v_loss.append((epoch, loss.item()))
		if epoch % 10 == 0:
			print(f'epoch: {epoch}, loss = {loss.item():.5f}')
		# print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))

		# is [17602, 27]
		X_train_tensor = X_train_tensor.reshape([X_train_tensor.shape[0], 1, X_train_tensor.shape[1]])
		# now should be [17602, 1, 27]
	

	# now start the plotting
	epochs = [x[0] for x in epochs_v_loss]
	loss = [x[1] for x in epochs_v_loss]

	plt.plot(epochs, loss)
	plt.xlabel('Epochs')
	plt.ylabel('Loss')
	plt.title('Epochs vs Loss')
	plt.show()

	# now we want to validate the model
	# we want to see if the model can predict the next letter in the sequence

	# attemping to predict the next letter in the sequence
	# a = torch.tensor(alphas['a'])
	# a.reshape([1,27])
	# res = ltsm.fwd(a)

	validate_predict = ltsm.fwd(X_validate_tensor) # forward pass
	data_predict = validate_predict.data.numpy() # convert to numpy array

	# _X = X_validate_tensor.data.numpy()
	# _X = _X.reshape([_X.shape[0], _X.shape[2]])
	# plt.plot(_X, label='original')
	# plt.plot(data_predict, label='predict')
	# validate_set_size = len(X_validate_tensor)
	# plt.axvline(x=validate_set_size, c='r', linestyle='--') #size of the training set
	# # plt.title('original vs predict')
	# plt.title('Timeseries Prediction')
	# plt.show()

	torch.save(ltsm.state_dict(), 'ltsm_model.pt')

	predicted_words = []
	_tmp_word = []
	for i in range(len(data_predict)):
		max = np.argmax(data_predict[i])
		_tmp_word.append(list(alphas)[max])
		if list(alphas)[max] == '#':
			predicted_words.append(_tmp_word)
			_tmp_word = []
			
	predicted_words = [''.join(x) for x in predicted_words if x != ['#']]
	print("Predicted words: ")
	print(predicted_words)

main()

# EOF
