import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import numpy as np
from torch.utils.data import Subset

class Net0(nn.Module):
    def __init__(self):
        super(Net0, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 10, bias=True)
    def forward(self, x):
        x = F.relu(self.fc1(x))
        return x
class Net1(nn.Module):
    def __init__(self):
        super(Net1, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 256, bias=True)
        self.fc2 = nn.Linear(256, 10, bias=True)
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return x
class Net5(nn.Module):
    def __init__(self, hl = 0):
        super(Net5, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 512, bias=True)
        self.fc2 = nn.Linear(512, 256, bias=True)
        self.fc3 = nn.Linear(256, 128, bias=True)
        self.fc4 = nn.Linear(128, 64, bias=True)
        self.fc5 = nn.Linear(64, 32, bias=True)
        self.fc6 = nn.Linear(32, 10, bias=True)
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = F.relu(self.fc6(x))
        return x
    
def PrintResultTable(vals, formaters):
    for i in range(len(vals)):
        print("\hline ", end = "")
        for j in range(len(vals[i])):
            print(formaters[j].format(vals[i][j]), end = "")
            if j != len(vals[i]) - 1:
                print(" & ", end = "")
        print(" \\\\")
def get_data_loaders(train_data_percent, batch_size):
    transform = transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])

    full_train_set = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    num_train = len(full_train_set)
    indices = list(range(num_train))
    split = int(train_data_percent * num_train)

    train_idx, valid_idx = indices[:split], indices[split:]
    train_set = Subset(full_train_set, train_idx)
    test_set = Subset(full_train_set, valid_idx)

    train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader

def CreateNN(net, train_size=0.1, batch_size=64, epochs=40):
    ## train
    train_loader, test_loader = get_data_loaders(train_size, batch_size)

    optimizer = optim.SGD(net.parameters(), lr=1e-5, momentum=0.9)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = Variable(data), Variable(target)
            data = data.view(-1, 28*28)
            optimizer.zero_grad()
            net_out = net(data)
            loss = criterion(net_out, target)
            loss.backward()
            optimizer.step()
    # test
    res = []
    res.append(train_size)
    for loader in [train_loader, test_loader]:
        test_loss = 0
        correct = 0
        for data, target in loader:
            data, target = Variable(data), Variable(target)
            data = data.view(-1, 28 * 28)
            net_out = net(data)
            test_loss += criterion(net_out, target).data.item()
            pred = net_out.data.max(1)[1] 
            correct += pred.eq(target.data).sum()

        test_loss /= len(loader.dataset)
        res.append(test_loss)
        res.append(100. * correct / len(loader.dataset))
        res.append(len(loader.dataset))
    
    return res
nets = [Net0(), Net1(), Net5()]

for net in nets:
    print("-----------")
    vals = []
    for train_size in np.linspace(0.1, 0.9, 9):
        vals.append(CreateNN(net, train_size = train_size))
    PrintResultTable(vals, ["{:.1f}", "{:.4f}", "{:.2f}", "{}", "{:.4f}", "{:.2f}", "{}"])
