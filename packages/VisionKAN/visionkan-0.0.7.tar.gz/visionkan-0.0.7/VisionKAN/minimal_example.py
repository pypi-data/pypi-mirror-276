# test_script.py

import sys
import os

# Add the path to the Vision_KAN package to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'VisionKAN')))
import math
from VisionKAN import create_model,train_one_epoch, evaluate
import torch.optim as optim
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as none

KAN_model = create_model(
    model_name='deit_tiny_patch16_224_KAN',
    pretrained=False,
    hdim_kan=192,
    num_classes=100,
    drop_rate=0.0,
    drop_path_rate=0.05,
    img_size=32,
    batch_size=144
)

# dataset CIFAR10

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5,), (0.5,))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=144,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR100(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=144, shuffle=False, num_workers=2)


#optimizer
optimizer = optim.SGD(KAN_model.parameters(), lr=0.001, momentum=0.9)
criterion = torch.nn.CrossEntropyLoss()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
KAN_model.to(device)

#train using engine.py
for epoch in range(2):  # loop over the dataset multiple times

    for samples, targets in trainloader:
        samples = samples.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)
        outputs = KAN_model(samples)  
        loss = criterion(outputs, targets) 
        loss_value = loss.item()

        if not math.isfinite(loss_value):
            print("Loss is {}, stopping training".format(loss_value))
            sys.exit(1)

        optimizer.zero_grad()
        loss.backward()
# evaluate
test_stats = evaluate(testloader, KAN_model, device=device)
print(f"Accuracy of the network on the {len(testset)} test images: {test_stats['acc1']:.1f}%")

print('Finished Training')